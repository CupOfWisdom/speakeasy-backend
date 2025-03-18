def pretty_print(verify_obj):
    for face in verify_obj:
        for attr, vals in face.items():
            print(attr.upper())
            if(isinstance(vals, dict)):
                for sub_attr, sub_val in vals.items():
                    print(sub_attr.upper(), sub_val)
            else:
                print(vals)
            print()