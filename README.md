SYCM
==============
This is a Sublime Text 3 plugin aims at providing C/C++ IDE features such as semantic code completion, error highligting and goto definition.
[YCMD] is used as the backend server.

ONLY TESTED ON UBUNTU

Features
==============
- Semantic code completion,
    + Provide semantic completion proposals after '.', '->' and '::', done
    + Variable type indicator, not yet
- Error highligting
    + Show error hints in code, done
    + Show errors in panel, not yet
- goto definition, not yet

Installation
=============
[YCMD] is partially written in C/C++, so you must compile [YCMD] on your platform yourself or get a pre-compiled version. Then you need to copy the following files from compiled [YCMD] to `SYCM/server` folder.
```
ycmd/
third_party/
libclang.so
ycm_client_support.so
ycm_core.so
.ycm_extra_conf.py
```

Your SYCM folder should look like this,
```
.
├── lib
│   ├── utils.py
│   ├── ycmd_events.py
│   └── ycmd_handler.py
├── LICENSE
├── marker.png
├── README.md
├── server
│   ├── libclang.so
│   ├── third_party
│       └── ...
│   ├── ycm_client_support.so
│   ├── ycm_core.so
│   └── ycmd
│       ├── completers
│       ├── default_settings.json
│       ├── extra_conf_store.py
│       ├── handlers.py
│       ├── hmac_plugin.py
│       ├── identifier_utils.py
│       ├── __init__.py
│       ├── __main__.py
│       ├── request_validation.py
│       ├── request_wrap.py
│       ├── responses.py
│       ├── responses.pyc
│       ├── server_state.py
│       ├── server_utils.py
│       ├── tests
│       ├── user_options_store.py
│       ├── utils.py
│       └── watchdog_plugin.py
└── sycmcompletion.py
```

[Windows x64 Install Guild](https://github.com/ivankoster/SublimeYouCompleteMe#installation-for-64bit-windows) provides an approach for Windows users.



Some codes are from [YcmdCompletion]

License
==============
Copyright 2015 Glyme Water. Licensed under the MIT License.

[YCMD]: https://github.com/Valloric/ycmd
[YcmdCompletion]: https://github.com/LuckyGeck/YcmdCompletion