### Installation

Using `install.sh` or:

**Build from source**
```sh
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
maturin build --release --strip -i python3.9 
pip install [.whl]
```

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgement
The main framework is from [REST](https://github.com/FasterDecoding/REST)


