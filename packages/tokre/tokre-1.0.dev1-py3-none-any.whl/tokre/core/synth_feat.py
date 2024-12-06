import torch.nn as nn
import tokre
from tokre.core.modules import PartialMatch, EmbedData
from tokre.core.parsing import parse
from tokre.core.tree_to_module import compile

from schedulefree import AdamWScheduleFree
import numpy as np
import torch
from frozendict import frozendict

from typing import Iterable

# import ray
from tqdm import tqdm

# Initialize Ray, using most available CPUs and ignoring reinit errors
# import multiprocessing
# num_cpus = max(1, multiprocessing.cpu_count() - 1)  # Leave one CPU free
# ray.init(ignore_reinit_error=True)#, _temp_dir="/media/noa/nvme_ssd/tmp")

def collect_matches(module, toks, aggr="longest"):
    assert aggr in ["shortest", "longest"]
    starting_matches = [
        PartialMatch(
            name="start",
            start=start_idx,
            end=start_idx,
            defns=frozendict(),
            data=None,
        )
        for start_idx in range(len(toks))
    ]

    unaggregated_matches = [
        match
        for start_match in starting_matches
        for match in module.matches(toks, start_match, reversed=False)
    ]

    end_to_aggr_match = {}
    for match in unaggregated_matches:
        if match.end in end_to_aggr_match:
            aggr_match = end_to_aggr_match[match.end]
            if len(match) > len(aggr_match):
                end_to_aggr_match[match.end] = match
        else:
            end_to_aggr_match[match.end] = match

    return list(end_to_aggr_match.values())


def is_int_or_tuple_of_ints(data):
    return isinstance(data, int) or (
        isinstance(data, tuple) and all([isinstance(x, int) for x in data])
    )


from tokre.core.modules import is_pred_data, Embed


def pred(module, match_data):
    assert is_pred_data(match_data) or (
        isinstance(module, Embed)
        and isinstance(match_data, int)
        or isinstance(match_data, tuple)
    )
    assert hasattr(module, "name")

    if isinstance(module, Embed):
        assert (
            isinstance(match_data, int)
            or isinstance(match_data, tuple)
            and all([isinstance])
        )
        return module.embed[match_data]

    if isinstance(match_data, list):
        assert hasattr(module, "mixer"), module
        preds = [torch.tensor(1.0)] + [pred(module, data) for data in match_data]
        preds = torch.stack(preds)

        return module.mixer(preds)

    elif isinstance(match_data, PartialMatch) or isinstance(match_data, EmbedData):
        match = match_data

        assert hasattr(module, "name_to_submodule")
        assert match.name in module.name_to_submodule, (module.name, match.name)
        return pred(module.name_to_submodule[match.name], match.data)

    elif match_data is None:
        return torch.tensor(1.0)

    else:
        raise ValueError("Unexpected match_data", match_data)


# @ray.remote(num_cpus=1)
# class ParallelModule:
#     def __init__(self, module, aggr, tokenizer):
#         self.module = module
#         self.aggr = aggr
#         print('initializing parallel module')
#         import tokre
#         tokre.setup(tokenizer=tokenizer)
#         print('initialized')

#     def get_matches(self, docs):
#         assert not isinstance(docs[0], str) and isinstance(docs[0], Iterable)
#         matches = [
#             collect_matches(self.module, toks=doc, aggr=self.aggr) for doc in docs
#         ]
#         return matches


class SynthFeat(nn.Module):
    def __init__(self, script, aggr="longest", n_actors=10, batch_size=100):
        super().__init__()
        assert aggr in ["longest", "shortest"]
        self.module = tokre.compile(script)
        self.aggr = aggr
        self.optimizer = AdamWScheduleFree(self.module.parameters(), lr=1e-3)

        self.batch_size = batch_size

    def get_matches(self, toks: list[str], n_matchers=1):
        assert n_matchers = 1          
        if isinstance(toks[0], list) or (
            isinstance(toks, np.ndarray) and len(toks.shape) == 2
        ):
            # toks is a list of documents
            docs = toks
            # if n_matchers > 1:
            #     print('creating parallel matchers')
            #     # module_ref = ray.put(self.module)
            #     # tokenizer_ref = ray.put(tokre.get_tokenizer())
            #     # tokre_ref = ray.put(tokre)
            #     parallel_matchers = [
            #         ParallelModule.remote(module_ref, self.aggr, tokenizer_ref) for _ in range(n_matchers)
            #     ]
            #     print('created parallel matchers')
            #     batched_docs = [
            #         docs[i : i + self.batch_size]
            #         for i in range(0, len(docs), self.batch_size)
            #     ]
            #     print('created batches')
            #     batched_matches = []
            #     K = 1  # Number of batches to process before waiting
            #     for i in range(0, len(batched_docs), K * len(parallel_matchers)):
            #         batch_futures = [
            #             parallel_matchers[j % len(parallel_matchers)].get_matches.remote(batched_docs[i + j])
            #             for j in range(min(K * len(parallel_matchers), len(batched_docs) - i))
            #         ]
            #         batched_matches.extend(ray.get(batch_futures))
            #     print('got matches')
            #     per_doc_matches = [match for batch in batched_matches for match in batch]
            #     return per_doc_matches
            # else:
            pbar = tqdm(docs, desc='collecting matches')
            per_doc_matches = [collect_matches(self.module, toks=doc, aggr=self.aggr) for doc in pbar]
            return per_doc_matches

        matches = collect_matches(self.module, toks=toks, aggr=self.aggr)
        return matches

    def get_mask(self, toks: Iterable, n_matchers=1):
        if isinstance(toks[0], Iterable) and not isinstance(toks[0], str):
            # toks is a list of documents
            assert all([isinstance(tok, str) for tok in toks[0]])
            matches = self.get_matches(toks, n_matchers=n_matchers)
            mask = torch.zeros((len(toks), len(toks[0])))
            for doc_idx, doc_matches in enumerate(matches):
                for match in doc_matches:
                    mask[doc_idx, match.end - 1] = 1.0
            return mask
        else:
            matches = self.get_matches(toks, n_matchers=1)
            mask = torch.zeros(len(toks))
            for match in matches:
                mask[match.end - 1] = 1.0

        return mask

    @torch.no_grad()
    def get_acts(self, toks, n_matchers=1):
        if isinstance(toks, Iterable) and isinstance(toks[0], str):
            synth_acts = torch.zeros(len(toks))
            matches = self.get_matches(toks, n_matchers=n_matchers)
            for match in matches:
                prediction = pred(self.module, match.data)
                synth_acts[match.end - 1] = prediction
        else:
            assert isinstance(toks, Iterable)
            assert isinstance(toks[0], Iterable)
            # return torch.stack([self.get_acts(doc) for doc in toks], dim=0)
            synth_acts = torch.zeros((len(toks), len(toks[0])))
            doc_matches = self.get_matches(toks, n_matchers=n_matchers)
            for doc_idx, matches in enumerate(doc_matches):
                for match in matches:
                    with torch.no_grad():
                        prediction = pred(self.module, match.data)
                        synth_acts[doc_idx, match.end-1] = prediction
        
        return synth_acts


    def train(self, toks, acts, parallel=True):
        from noa_tools import see
        print("getting matches")
        all_matches = self.get_matches(toks, parallel=parallel)
        print("training")
        for doc_matches, doc_acts in tqdm(zip(all_matches, acts)):
            for match in doc_matches:
                act = doc_acts[match.end - 1]
            
                loss = (pred(self.module, match.data) - act)**2

                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()

    @property
    def pyregex(self):
        return self.module.pyregex
