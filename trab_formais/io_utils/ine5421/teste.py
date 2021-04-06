import tree

# t = tree.Tree(['a', 'b']).make_tree('a(a|b)*a#')
t = tree.Tree(['a', 'b']).make_tree('aa*(bb*aa*b)*#')
# t = tree.Tree(['a', 'b', '&']).make_tree('(&|b)(ab)*(&|a)#')
print(t)
