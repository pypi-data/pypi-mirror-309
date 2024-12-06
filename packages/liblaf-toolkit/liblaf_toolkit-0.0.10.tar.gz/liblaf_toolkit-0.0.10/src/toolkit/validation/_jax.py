import jax.numpy as jnp
import pydantic

Jax = pydantic.BeforeValidator(jnp.asarray)
