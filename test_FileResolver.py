#!/usr/bin/env python

from ignf_gpf_api.action.FileResolver import FileResolver

# creer une instance ResolverError
test_FileResolver = FileResolver("file")

print("type str")
s_test_str: str = test_FileResolver.resolve("str(tests/_data/action/FileResolver/text.txt)")
print(s_test_str)
print("type list")
s_test_list: str = test_FileResolver.resolve("list(tests/_data/action/FileResolver/list.json)")
print(s_test_list)
print("type dict")
s_test_dict = test_FileResolver.resolve("dict(tests/_data/action/FileResolver/dict.json)")
print(s_test_dict)
