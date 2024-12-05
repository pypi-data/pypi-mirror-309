import pydantic

import toolkit as tk

DictOfNumpy = pydantic.BeforeValidator(tk.as_dict_of_numpy)
Numpy = pydantic.BeforeValidator(tk.as_numpy)
