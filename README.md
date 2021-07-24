# Odak
[![DOI](https://zenodo.org/badge/3987171.svg)](https://zenodo.org/badge/latestdoi/3987171)

Odak (pronounced "O-dac") is the fundamental library for scientific computing in optical sciences. Odak includes modules for geometric [3D raytracing](odak/raytracing/), [Jones calculus](odak/jones), [beam propagation and wave optics](odak/wave) among with [a set of tools](odak/tools) to ease your pain in [measurement](odak/measurement), [exporting/importing CAD](odak/tools/asset.py), and [visualization](odak/visualize) during a design process. We have generated a set of recipes that goes well with machine learning approaches compatible with `torch` learning framework, which can also be found [here](odak/learn). We have created a bunch of [test scripts](test/) for inspiring the way you use odak and helping your design process. For computationally expensive tasks, we have created a [distribution system](odak/manager) to process tasks in parallel across multiple computing resources within the same network. Odak can either run using CPUs or can switch to [NVIDIA GPUs](odak/__init__.py#L8) automatically.

## Getting Started

### Installing
Odak can be installed using [pip](https://pypi.org/project/pip):

```bash
pip3 install git+https://github.com/kunguz/odak
```

or:

```bash
pip3 install odak
```

### Usage
It is easy as in this recorded session. Import it to your code and start designing your next in Optics!

![alt tag](example.gif)

## Citing
If you use Odak in a research project leading to a publication, please acknowledge this fact by using our [bibtex citation entry generated by Zenodo](https://zenodo.org/record/5035579).

## Contributing
Perhaps the best way is checking the issues section as a starter. If you have a specific point in mind and can't find it in the issues section, starting an issue accordingly is an another good starting point. If you think you have bigger plans in mind, here is my email **kaanaksit at kaanaksit dot com**.
