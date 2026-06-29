#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <algorithm>
#include <string>
#include <vector>

namespace py = pybind11;

// ---------------------------------------------------------------------------
// Domain struct — mirrors the fields on SiteDTO that matter for scoring
// ---------------------------------------------------------------------------
struct SiteScore {
    std::string name;
    std::string region;
    std::string status;
    double      score;
};

// ---------------------------------------------------------------------------
// Scoring formula
//   score = 0.4 * (cpu_capacity / 10 000) + 0.6 * (storage_tb / 1 000)
//
// Both terms are normalised so neither dominates at typical WLCG-scale values.
// Offline sites are penalised to the bottom; degraded sites are penalised by 50%.
// ---------------------------------------------------------------------------
static double compute_score(int cpu, double storage_tb, const std::string& status) {
    double raw = 0.4 * (static_cast<double>(cpu) / 10000.0)
               + 0.6 * (storage_tb / 1000.0);

    if (status == "offline")  return -1.0;
    if (status == "degraded") return raw * 0.5;
    return raw;
}

// ---------------------------------------------------------------------------
// rank_sites — main entry point exposed to Python
//
// Takes parallel vectors (matching indices) from the caller.
// Returns a new vector sorted by score descending.
// ---------------------------------------------------------------------------
std::vector<SiteScore> rank_sites(
    const std::vector<std::string>& names,
    const std::vector<std::string>& regions,
    const std::vector<std::string>& statuses,
    const std::vector<int>&         cpus,
    const std::vector<double>&      storage
) {
    if (names.size() != cpus.size() || names.size() != storage.size()) {
        throw std::invalid_argument("All input vectors must have the same length.");
    }

    std::vector<SiteScore> results;
    results.reserve(names.size());

    for (std::size_t i = 0; i < names.size(); ++i) {
        results.push_back({
            names[i],
            regions[i],
            statuses[i],
            compute_score(cpus[i], storage[i], statuses[i])
        });
    }

    std::sort(results.begin(), results.end(),
              [](const SiteScore& a, const SiteScore& b) {
                  return a.score > b.score;
              });

    return results;
}

// ---------------------------------------------------------------------------
// pybind11 module definition
// ---------------------------------------------------------------------------
PYBIND11_MODULE(site_scorer, m) {
    m.doc() = "C++ site scoring and ranking extension for CRIC-SiteRegistry";

    py::class_<SiteScore>(m, "SiteScore")
        .def_readonly("name",    &SiteScore::name)
        .def_readonly("region",  &SiteScore::region)
        .def_readonly("status",  &SiteScore::status)
        .def_readonly("score",   &SiteScore::score)
        .def("__repr__", [](const SiteScore& s) {
            return "<SiteScore name=" + s.name
                 + " score=" + std::to_string(s.score) + ">";
        });

    m.def(
        "rank_sites",
        &rank_sites,
        py::arg("names"),
        py::arg("regions"),
        py::arg("statuses"),
        py::arg("cpus"),
        py::arg("storage"),
        R"pbdoc(
            Rank computing sites by a weighted CPU + storage score.

            Parameters
            ----------
            names    : list[str]   — site names
            regions  : list[str]   — site regions
            statuses : list[str]   — "online" | "degraded" | "offline"
            cpus     : list[int]   — cpu_capacity values
            storage  : list[float] — storage_tb values

            Returns
            -------
            list[SiteScore] sorted by score descending.
            Offline sites always appear last (score = -1.0).
            Degraded sites score at 50% of their raw value.
        )pbdoc"
    );
}