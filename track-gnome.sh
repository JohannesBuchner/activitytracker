#!/bin/bash
# 
# Tracks what you are spending your time on
# 
#
# Copyright (c) 2019 Johannes Buchner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

DIR=$HOME/.local/share/activitytracker/
mkdir -p $DIR

if [ -e $DIR/pid ]
then
	pid=$(cat $DIR/pid)
	# check if still running
	if kill -0 ${pid} 2>/dev/null
	then		
		# check if related
		if grep -q $0 /proc/${pid}/cmdline
		then
			echo "activity tracker already runnning as PID=$pid"
			exit 0
		fi
	fi
fi

pid=$$
echo $pid > $DIR/pid

function window_call_info {
	# call Gnome extension "Window Calls extended" 
	# https://extensions.gnome.org/extension/4974/window-calls-extended/
	# needs to be installed!
	gdbus call --session --dest org.gnome.Shell --object-path /org/gnome/Shell/Extensions/WindowsExt --method org.gnome.Shell.Extensions.WindowsExt.$1 | 
	sed -n "s/^('\(.*\)',)$/\1/g; s/['\"]//g; p"
}

while true
do
echo '{"timestamp":'$(date +%s)',"windowname":"'$(window_call_info FocusTitle)'","exe":"'$(window_call_info FocusClass)'"}';
sleep 10;
done >> $DIR/log
