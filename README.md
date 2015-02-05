SYCM (SublimeYouCompleteMe)
==============
This is a Sublime Text 3 plugin aims at providing C/C++ IDE features such as semantic code completion, error highligting, goto definition and more.
[YCMD] is used as the backend server.

ONLY TESTED ON UBUNTU

Features
==============
- Semantic code completion,
    + Provide semantic completion proposals on `.`, `->` and `::`, done
    + Variable type indicator, not yet
- Error highligting
    + Show error hints in code, done
    + Show errors in panel, done
    + Jump to corresponding error in source when clicking problems panel, not yet.
- Goto definition, done

![demo](https://raw.githubusercontent.com/glymehrvrd/SYCM/compiled-ycmd/demo.gif)

Installation
=============

Set up YCMD
-------------
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
├── commands
├── lib
├── listeners
└── server    <----- create and put compiled ycmd into this folder
    ├── third_party
    └── ycmd
```

[Windows x64 Install Guild](https://github.com/ivankoster/SublimeYouCompleteMe#installation-for-64bit-windows) provides an approach for Windows users to get compiled ycmd.

Ubuntu amd64 users can find compiled ycmd here. [https://github.com/glymehrvrd/SYCM/tree/compiled-ycmd](https://github.com/glymehrvrd/SYCM/tree/compiled-ycmd).

Set Sublime Config
--------------
To enable prompt on `.`, `->` and `::`, you need to add the following configure to your sublime setting. Or create a file named `C++.sublime-settings` in `Packages/User` with following as its content.
```JSON
"auto_complete_triggers":
[
    {
        "characters": ".:>",
        "selector": "source.c++ - string - comment - constant.numeric"
    }
]
```


Some codes are from [YcmdCompletion].

License
==============
Copyright 2015 Glyme Water. Licensed under the MIT License.

[YCMD]: https://github.com/Valloric/ycmd
[YcmdCompletion]: https://github.com/LuckyGeck/YcmdCompletion