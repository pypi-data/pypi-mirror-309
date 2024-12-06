from dataclasses import dataclass


@dataclass
class PARAM:
    name: str
    value: str


@dataclass
class ATTRIBUTE:
    name: str
    text: str
    type: str = ""


@dataclass
class VARIABLE:
    tag: str
    sourceName: str
    destinationName: str
    dataType: str
    attributes: list[ATTRIBUTE] | None
    source_attributes: list[ATTRIBUTE] | None


@dataclass
class DATASET:
    type: str
    datasetID: str
    active: str
    datasets: list | None
    params: list[PARAM] | None
    attributes: list[ATTRIBUTE] | None
    source_attributes: list[ATTRIBUTE] | None
    variables: list[VARIABLE] | None


@dataclass
class ERDDAP:
    params: list[PARAM]
    datasets: list[DATASET]
    parent_child: list[tuple[2]]


def print_dataset(dataset: DATASET, indent: int):
    indent_str = " ".join(["" for i in range(indent)])
    print()
    print("dataset:")
    print(f"{indent_str} datasetID: {dataset.datasetID}")
    print(f"{indent_str} type: {dataset.type}")
    print(f"{indent_str} active: {dataset.active}")
    print(f"{indent_str} datasets:")
    for d in dataset.datasets:
        print_dataset(d, indent + 2)
    print(f"{indent_str} params:")
    for p in dataset.params:
        print(f"{indent_str}  {p}")
    print(f"{indent_str} attributes:")
    for a in dataset.attributes:
        print(f"{indent_str}  {a}")
    print(f"{indent_str} variables:")
    for v in dataset.variables:
        print(f"{indent_str}  {v.tag} {v.dataType} {v.destinationName} {v.sourceName}")
        print(f"{indent_str}   attributes:")
        for a in dataset.attributes:
            print(f"{indent_str}    {a}")
