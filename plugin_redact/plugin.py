import os
import re
import shutil
import sys
from mkdocs.plugins import BasePlugin

REDACT_PATTERN = re.compile(r"<!--\s*REDACT\s*-->(.*?)<!--\s*REDACTEND\s*-->", re.DOTALL)

class RedactPlugin(BasePlugin):

	def on_pre_build(self, config):
		"""
		Check if we are running 'mkdocs build' once at the start.
		We store this so we don't check on every single page.
		"""
		self.is_build = "build" in sys.argv
		
		if self.is_build:
			print("✅ Redaction will be applied for this build.")
		else:
			print("ℹ️ Redaction skipped: 'build' command not detected (e.g., 'serve').")

	def on_page_markdown(self, markdown, page, config, files):
		"""
		Called for each Markdown page.
		We apply the redaction here if self.is_build is True.
		"""
		
		# If 'self.is_build' was set to True in on_pre_build, redact
		if getattr(self, 'is_build', False):
			return REDACT_PATTERN.sub("**REDACTED**", markdown)
		
		# Otherwise, return the markdown untouched
		return markdown