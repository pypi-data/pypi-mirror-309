GEN_TYPING_TARGETS += src/toolkit/array/array_like/__init__.pyi
GEN_TYPING_TARGETS += src/toolkit/array/array_like/_bool.py
GEN_TYPING_TARGETS += src/toolkit/array/array_like/_float.py
GEN_TYPING_TARGETS += src/toolkit/array/array_like/_integer.py
GEN_TYPING_TARGETS += src/toolkit/array/jax/__init__.pyi
GEN_TYPING_TARGETS += src/toolkit/array/jax/_bool.py
GEN_TYPING_TARGETS += src/toolkit/array/jax/_export.py
GEN_TYPING_TARGETS += src/toolkit/array/jax/_float.py
GEN_TYPING_TARGETS += src/toolkit/array/jax/_integer.py
GEN_TYPING_TARGETS += src/toolkit/array/numpy/__init__.pyi
GEN_TYPING_TARGETS += src/toolkit/array/numpy/_bool.py
GEN_TYPING_TARGETS += src/toolkit/array/numpy/_export.py
GEN_TYPING_TARGETS += src/toolkit/array/numpy/_float.py
GEN_TYPING_TARGETS += src/toolkit/array/numpy/_integer.py
GEN_TYPING_TARGETS += src/toolkit/array/torch/__init__.pyi
GEN_TYPING_TARGETS += src/toolkit/array/torch/_bool.py
GEN_TYPING_TARGETS += src/toolkit/array/torch/_export.py
GEN_TYPING_TARGETS += src/toolkit/array/torch/_float.py
GEN_TYPING_TARGETS += src/toolkit/array/torch/_integer.py

.PHONY: $(GEN_TYPING_TARGETS)
gen-array-types: $(GEN_TYPING_TARGETS)
	@ ruff check $^

# ----------------------------- Auxiliary Targets ---------------------------- #

$(GEN_TYPING_TARGETS): src/toolkit/%: templates/%.jinja scripts/gen-array-types.py
	@ python scripts/gen-array-types.py --output "$@" "$<"
