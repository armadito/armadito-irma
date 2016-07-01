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

import re
import os
import sys
import locale
import logging

from subprocess import Popen, PIPE

log = logging.getLogger(__name__)


class ArmaditoPDF(object):

	@staticmethod
	def build_cmd(cmd, *args):
		cmd = [cmd]
		for param in args:
			if isinstance(param, (tuple, list)):
				cmd.extend(param)
			else:
				cmd.append(param)
		return " ".join(cmd)

	@staticmethod
	def run_cmd(cmd):		
		# remove whitespace with re.sub, then split()
		re.sub(r'\s+', ' ', cmd)
        cmdarray = cmd.split()
        # execute command with popen, clean up outputs
        pd = Popen(cmdarray, stdout=PIPE, stderr=PIPE)
        raw_stdout, stderr = map(lambda x: x.strip() if x.strip() else None, pd.communicate())

		retcode = pd.returncode

		stdout = raw_stdout
		print"retcode = ", retcode
		# return tuple (retcode, out, err)
		return (retcode, stdout, stderr)


	@staticmethod
	def get_a6oPDF_path():
		binpath = os.path.join('/opt/armadito/armadito-pdf/tools/cli_analyzer/','a6oPDFAnalyzer')        		
		return binpath if os.path.exists(binpath) else None


	# Check analysis results
	def check_analysis_results(self, paths, results):
		retcode, stdout, stderr = results
		# check stdout
		if stdout:

			match = re.search(r'Coef = (?P<coef>[^\s])',stdout)            

			if match:
				#print "dbg :: coef = ", match.group('coef');
				results = stdout
				error = None
			else:
				results = None
				error = stdout


		# uniformize retcode (1 is success)
		retcode = 1 if results else 0
		if not results:
			results = None
		return retcode, results, error


	# Launch an analysis
	def analyze(self, paths):
		cmd = self.build_cmd(self.get_a6oPDF_path(), paths)
		results = self.run_cmd(cmd)
		return self.check_analysis_results(paths, results)
