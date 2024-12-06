# Changelog

## [0.0.10](https://github.com/liblaf/python-toolkit/compare/v0.0.9...v0.0.10) (2024-11-17)


### ♻ Code Refactoring

* replace external validation with internal toolkit validation ([f892bca](https://github.com/liblaf/python-toolkit/commit/f892bca7cf16557a4d1e75611b8372742d55f543))
* streamline import aliases and improve serialization module ([7a4f444](https://github.com/liblaf/python-toolkit/commit/7a4f444ebb710930f26b188293206567f8aee238))

## [0.0.9](https://github.com/liblaf/python-toolkit/compare/v0.0.8...v0.0.9) (2024-11-16)


### ♻ Code Refactoring

* reorganize imports and update module list ([5a9a419](https://github.com/liblaf/python-toolkit/commit/5a9a41934f5271b6888cc5658482ec85a0b281de))

## [0.0.8](https://github.com/liblaf/python-toolkit/compare/v0.0.7...v0.0.8) (2024-11-14)


### ✨ Features

* add support for scalar conversion across array libraries ([5dc0057](https://github.com/liblaf/python-toolkit/commit/5dc0057ad51886279bdf814c32f2c9e9aea18e55))
* introduce lazy loading for ABC module ([133d46a](https://github.com/liblaf/python-toolkit/commit/133d46add64d1988386554038ace106ab7d02625))

## [0.0.7](https://github.com/liblaf/python-toolkit/compare/v0.0.6...v0.0.7) (2024-11-14)


### ♻ Code Refactoring

* reorganize toolkit modules for better modularity ([5809983](https://github.com/liblaf/python-toolkit/commit/5809983ee4b21dec1141ef5b5c568e48199c5e0e))


### 👷 Build System

* update dependency installation command in CI configuration ([cd10c17](https://github.com/liblaf/python-toolkit/commit/cd10c1722e3dae97ad3201c2c6eb25574bd7e8ce))

## [0.0.6](https://github.com/liblaf/python-toolkit/compare/v0.0.5...v0.0.6) (2024-11-14)


### ♻ Code Refactoring

* reorganize array types and validation modules ([353b241](https://github.com/liblaf/python-toolkit/commit/353b2418b8fd61ea29d1abb19041a8de30c2403f))

## [0.0.5](https://github.com/liblaf/python-toolkit/compare/v0.0.4...v0.0.5) (2024-11-14)


### 📝 Documentation

* establish documentation infrastructure and initial setup ([7340211](https://github.com/liblaf/python-toolkit/commit/73402118e80a514f4748e0622157a23597b78385))


### ♻ Code Refactoring

* reorganize imports and add new modules for enhanced type handling ([3301191](https://github.com/liblaf/python-toolkit/commit/330119116362406bb125ed6ef3ea702b48d14274))


### 👷 Build System

* update dependency management and build configurations ([a8856e9](https://github.com/liblaf/python-toolkit/commit/a8856e97448cebb9a9c0425d113231575ac1d754))

## [0.0.4](https://github.com/liblaf/python-toolkit/compare/v0.0.3...v0.0.4) (2024-11-14)


### ♻ Code Refactoring

* rename module and update references ([06e8f88](https://github.com/liblaf/python-toolkit/commit/06e8f886445c5cbb893df8986c99487379d8a2cb))
* streamline environment variable handling and module imports ([5bc61f1](https://github.com/liblaf/python-toolkit/commit/5bc61f1883a4f0ebf2628d0470b5f19457377cfa))

## [0.0.3](https://github.com/liblaf/python-toolkit/compare/v0.0.2...v0.0.3) (2024-11-11)


### 🐛 Bug Fixes

* update .gitignore to include env file ([2feec03](https://github.com/liblaf/python-toolkit/commit/2feec03a36ec2b52b7f1923c27fc8c75616c5c46))

## [0.0.2](https://github.com/liblaf/python-toolkit/compare/v0.0.1...v0.0.2) (2024-11-11)


### 👷 Build System

* configure Pyright for dependency installation and linting ([70bc996](https://github.com/liblaf/python-toolkit/commit/70bc996c89a09f0eeb27a27a0ce09e5cd7ca139f))


### 🔧 Continuous Integration

* add concurrency control to CI workflows ([0e6cb92](https://github.com/liblaf/python-toolkit/commit/0e6cb92a65c821e699633e410f94a8953d66d19b))
* streamline CI workflow for main branch ([16a61a3](https://github.com/liblaf/python-toolkit/commit/16a61a390fba3f2b8c2717f096f3aa332cde9b4c))

## [0.0.1](https://github.com/liblaf/python-toolkit/compare/v0.0.0...v0.0.1) (2024-11-11)


### ✨ Features

* add logging functionality for additional experiment data ([b0ea8fb](https://github.com/liblaf/python-toolkit/commit/b0ea8fb1e4845e9f198d365c5226fd0777ebfcd2))


### ♻ Code Refactoring

* **exp:** reorganize experiment module for clarity and maintainability ([24373c0](https://github.com/liblaf/python-toolkit/commit/24373c03cefa8743d9e52f2e6389bff18238879d))


### 🔧 Continuous Integration

* enable write permissions for GitHub Actions OIDC tokens ([0d5a367](https://github.com/liblaf/python-toolkit/commit/0d5a3671b291f9de61f1c2bbdb5807d518681964))

## 0.0.0 (2024-11-11)


### ✨ Features

* add support for Nx4 array types across all array libraries ([47dbb2c](https://github.com/liblaf/python-toolkit/commit/47dbb2c222a4e0225e5a6a5d7aad091f4db253d3))
* enhance experiment logging and configuration ([6865d76](https://github.com/liblaf/python-toolkit/commit/6865d769c9e0ea5a8dd0d49ea65820c4ab8530ff))
* implement array type handling for JAX, NumPy, and PyTorch ([fd7d97a](https://github.com/liblaf/python-toolkit/commit/fd7d97a43f68be0a8364a9e533b524a1094c9949))
* integrate comet-ml for experiment tracking and add environment variable utilities ([96ddd0e](https://github.com/liblaf/python-toolkit/commit/96ddd0ee332f903478deef1dc8b254fbb4334ece))
* introduce base parameters for experiments ([a12d637](https://github.com/liblaf/python-toolkit/commit/a12d637d9fe599708e158a1e870bdd367d78e9e8))
* introduce new utility modules and enhance logging ([38bf1b4](https://github.com/liblaf/python-toolkit/commit/38bf1b4a57594b156a0c10947723df00411c669a))


### 🐛 Bug Fixes

* correct tqdm dependency version to avoid bug ([6cc811c](https://github.com/liblaf/python-toolkit/commit/6cc811c62e2eb4bcab64d63d2b4cd5d61385f940))


### ♻ Code Refactoring

* enhance array type handling by adding conversion utilities ([ce1f8ee](https://github.com/liblaf/python-toolkit/commit/ce1f8eebf31a0a55ae0fffe301dfb151bfba039d))
* **exp:** rename BaseParams to BaseConfig for clarity and consistency ([c54bab2](https://github.com/liblaf/python-toolkit/commit/c54bab290601373d1b8d3c453468acd2242c816c))
* reorganize imports and update log file names ([cec13d5](https://github.com/liblaf/python-toolkit/commit/cec13d519fea056be48dcf29639637dcb12c074e))
* standardize array shape notation in type annotations ([24d3011](https://github.com/liblaf/python-toolkit/commit/24d30119ba119ae1972b4c852f018ffc29ca1e0d))


### 🔧 Continuous Integration

* configure default settings for Python linter ([0441145](https://github.com/liblaf/python-toolkit/commit/0441145ad1cda5e557451446e336c083cf15b394))
* enable concurrency control to cancel in-progress workflows ([bd4f084](https://github.com/liblaf/python-toolkit/commit/bd4f084d7fcbe7de7b0569e4c1a81b4894cd2aae))
* ensure build job completion before release and pre-release jobs ([747f356](https://github.com/liblaf/python-toolkit/commit/747f35656630516e2e2cc9170e010bd5900586fc))
* remove uv.lock to prevent CI failure due to unavailable PyPI mirror ([a7f28af](https://github.com/liblaf/python-toolkit/commit/a7f28af6806663ccd6412952dbb3940b224e8d1b))
* set up continuous integration and release workflows ([e34cf2a](https://github.com/liblaf/python-toolkit/commit/e34cf2ae0213c532353cfabe62ecafa4104910a0))
