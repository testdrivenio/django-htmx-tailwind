from django.contrib import admin

from compressor.filters import CompilerFilter


class PostCSSFilter(CompilerFilter):
    command = "postcss"