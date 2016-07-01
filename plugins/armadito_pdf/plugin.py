#
# Copyright (c) 2013-2016 Quarkslab.
# Copyright (c) 2016 Teclib'
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the top-level directory
# of this distribution and at:
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# No part of the project, including this file, may be copied,
# modified, propagated, or distributed except according to the
# terms contained in the LICENSE file.

import os
import sys

from datetime import datetime
from lib.common.utils import timestamp
from lib.plugins import PluginBase
from lib.plugins import FileDependency
from lib.plugins import BinaryDependency
from lib.plugins import PlatformDependency
from lib.plugin_result import PluginResult
from lib.irma.common.utils import IrmaProbeType


class ArmaditoPDFPlugin(PluginBase):

	class ArmaditoPDFResults:
		ERROR = -1
		FAILURE = 0
		SUCCESS = 1

	_plugin_name_ = "ArmaditoPDF"
	_plugin_display_name_ = "Armadito PDF analyzer"
	_plugin_author_ = "Teclib <ufausther@teclib.com>"
	_plugin_version_ = "1.0.0"
	_plugin_category_ = IrmaProbeType.metadata
	_plugin_description_ = "Plugin to analyze pdf documents"
	_plugin_mimetype_regexp = 'PDF'
	_plugin_dependencies_ = [
		PlatformDependency('linux'),
		BinaryDependency('/opt/armadito/armadito-pdf/tools/cli_analyzer/a6oPDFAnalyzer'),
	]


	def __init__(self):
		module = sys.modules['modules.metadata.armadito_pdf.a6o_pdf'].ArmaditoPDF
		self.module = module()


	def run(self, paths):
		results = PluginResult(
					name=type(self).plugin_display_name,
					type=type(self).plugin_category,
					version=None)
                               
		# launch file analysis
		try:
			started = timestamp(datetime.utcnow())
			results.status, results.results, results.error = self.module.analyze(paths)
			stopped = timestamp(datetime.utcnow())
			results.duration = stopped - started
		except Exception as e:
			results.status = self.ArmaditoPDFResults.ERROR
			results.error = str(e)
		return results
