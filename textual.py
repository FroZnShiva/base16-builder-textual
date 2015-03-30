#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil
from argparse import ArgumentParser
from ConfigParser import SafeConfigParser

def printerror(msg):
	print >> sys.stderr, msg

def fatal(msg, exitcode = 1):
	printerror(msg)
	exit(exitcode)

def iterateFiles(path, callback, context = None):
	for subdir, dirs, files in os.walk(path):
		for filename in files:
			absolute_file_path = os.path.join(subdir, filename)
			callback(absolute_file_path, context)

def copyFile(fromPath, toPath, filename):
	shutil.copy(os.path.join(fromPath, filename), os.path.join(toPath, filename))

class Base16:
	def __init__(self, configfile, variant):
		lvariant = variant.lower()
		parser = SafeConfigParser()
		parser.read(configfile)
		config = parser._sections['base16']

		self.variant = variant
		self.author = config['author']
		self.scheme = '%s %s' % (config['scheme'], variant)
		self.title = 'Base16 %s' % self.scheme
		self.base00 = config['base00']
		self.base01 = config['base01']
		self.base02 = config['base02']
		self.base03 = config['base03']
		self.base04 = config['base04']
		self.base05 = config['base05']
		self.base06 = config['base06']
		self.base07 = config['base07']
		self.base08 = config['base08'] # Red
		self.base09 = config['base09'] # Orange
		self.base0A = config['base0a'] # Yellow
		self.base0B = config['base0b'] # Green
		self.base0C = config['base0c'] # Aqua
		self.base0D = config['base0d'] # Blue
		self.base0E = config['base0e'] # Purple
		self.base0F = config['base0f'] # Brown

		if lvariant == 'dark':
			self.base00v = self.base07
			self.base01v = self.base06
			self.base02v = self.base05
			self.base03v = self.base04
			self.base04v = self.base03
			self.base05v = self.base02
			self.base06v = self.base01
			self.base07v = self.base00
		elif lvariant == 'light':
			self.base00v = self.base00
			self.base01v = self.base01
			self.base02v = self.base02
			self.base03v = self.base03
			self.base04v = self.base04
			self.base05v = self.base05
			self.base06v = self.base06
			self.base07v = self.base07
		else:
			fatal("Unknown variant: '%s'" % variant)

	def format(self, string):
		r = lambda x: int(x[0:2], 16)
		g = lambda x: int(x[2:4], 16)
		b = lambda x: int(x[4:6], 16)
		return string.format(
			author = self.author,
			scheme = self.scheme,
			title = self.title,
			variant = self.variant,

			base00 = self.base00v, base00fixed = self.base00,
			base01 = self.base01v, base01fixed = self.base01,
			base02 = self.base02v, base02fixed = self.base02,
			base03 = self.base03v, base03fixed = self.base03,
			base04 = self.base04v, base04fixed = self.base04,
			base05 = self.base05v, base05fixed = self.base05,
			base06 = self.base06v, base06fixed = self.base06,
			base07 = self.base07v, base07fixed = self.base07,
			base08 = self.base08,
			base09 = self.base09,
			base0A = self.base0A,
			base0B = self.base0B,
			base0C = self.base0C,
			base0D = self.base0D,
			base0E = self.base0E,
			base0F = self.base0F,

			base00r = r(self.base00v), base00g = g(self.base00v), base00b = b(self.base00v),
			base01r = r(self.base01v), base01g = g(self.base01v), base01b = b(self.base01v),
			base02r = r(self.base02v), base02g = g(self.base02v), base02b = b(self.base02v),
			base03r = r(self.base03v), base03g = g(self.base03v), base03b = b(self.base03v),
			base04r = r(self.base04v), base04g = g(self.base04v), base04b = b(self.base04v),
			base05r = r(self.base05v), base05g = g(self.base05v), base05b = b(self.base05v),
			base06r = r(self.base06v), base06g = g(self.base06v), base06b = b(self.base06v),
			base07r = r(self.base07v), base07g = g(self.base07v), base07b = b(self.base07v),
			base08r = r(self.base08), base08g = g(self.base08), base08b = b(self.base08),
			base09r = r(self.base09), base09g = g(self.base09), base09b = b(self.base09),
			base0Ar = r(self.base0A), base0Ag = g(self.base0A), base0Ab = b(self.base0A),
			base0Br = r(self.base0B), base0Bg = g(self.base0B), base0Bb = b(self.base0B),
			base0Cr = r(self.base0C), base0Cg = g(self.base0C), base0Cb = b(self.base0C),
			base0Dr = r(self.base0D), base0Dg = g(self.base0D), base0Db = b(self.base0D),
			base0Er = r(self.base0E), base0Eg = g(self.base0E), base0Eb = b(self.base0E),
			base0Fr = r(self.base0F), base0Fg = g(self.base0F), base0Fb = b(self.base0F),
		)

	def write(self, path, filename, data):
		f = open(os.path.join(path, filename), 'w')
		f.write(self.format(data))
		f.close()

class Settings:
	def __init__(self, output_path, preview, default_irc_colours, light, dark):
		self.output_path = output_path
		self.preview = preview
		self.default_irc_colours = default_irc_colours
		self.light = light
		self.dark = dark

def generateTextualStyle(base16, settings):
	path = os.path.join(settings.output_path, base16.title)

	if os.path.exists(path):
		shutil.rmtree(path)

	data_path = os.path.join(path, 'Data')
	settings_path = os.path.join(data_path, 'Settings')
	template_path = os.path.join(data_path, 'Templates')

	os.makedirs(settings_path)
	os.makedirs(template_path)

	design_css_data = design_css
	if not settings.default_irc_colours:
		design_css_data += irc_colours_css

	base16.write(path, 'copyright.txt', copyright_txt)
	base16.write(path, 'design.css', design_css_data)
	base16.write(settings_path, 'styleSettings.plist', stylesettings_plist)

	files_to_copy = [
		(path, 'scripts.js'),
		(template_path, 'encryptedMessageLock.mustache'),
	]

	for destination, filename in files_to_copy:
		copyFile('files', destination, filename)

	if settings.preview:
		base16.write(path, 'preview.html', preview_html)

	print('  - %s' % path)

def generateTextualStyles(filename, settings):
	if not filename.endswith('.cfg'):
		return

	if settings.light:
		generateTextualStyle(Base16(filename, 'Light'), settings)
	if settings.dark:
		generateTextualStyle(Base16(filename, 'Dark'), settings)

def main():
	parser = ArgumentParser(
		description = """
			This is a script which generates styles for the Textual IRC client
			based on the colour schemes of Base16 by chriskempson and the
			default Simplified style bundled with Textual.
		""",
	)
	variantGrp = parser.add_argument_group('variants')
	variantGrp.add_argument(
		'-l', '--light',
		help = """
			Only generate the light variant.
		""",
		action = 'store_true',
		default = False,
	)
	variantGrp.add_argument(
		'-d', '--dark',
		help = """
			Only generate the dark variant.
		""",
		action = 'store_true',
		default = False,
	)
	parser.add_argument(
		'--default-irc-colours',
		help = """
			This option disables replacing the default IRC colours to fit with 
			the Style. This means that the default IRC colours defined by
			Textual are used.
		""",
		action = 'store_true',
		default = False,
	)
	parser.add_argument(
		'-s', '--scheme',
		help = """
			Generate the style for a given scheme only. If this option is not
			given, styles for all Base16 schemes are generated. The schemes are
			stored in the 'schemes' subdirectory.
		""",
		action = 'store',
	)
	parser.add_argument(
		'-i', '--install',
		help = """
			This installs the generated style(s) directly into the location
			where the Textual styles are stored. If this is not set, the
			generated styles will be stored in the 'output' subdirectory.
		""",
		action = 'store_true',
		default = False,
	)
	parser.add_argument(
		'-p', '--preview',
		help = """
			If this is enabled preview files will be generated for each style.
			Usually you don't want to enable this.
		""",
		action = 'store_true',
		default = False,
	)
	args = parser.parse_args()

	output_path = 'output'
	config_path = 'schemes'
	install_path = os.path.expanduser('~/Library/Group Containers/8482Q6EPL6.com.codeux.irc.textual/Library/Application Support/Textual/Styles')

	if not os.path.exists(config_path):
		fatal('Missing configuration files, please run the base16 command first.')

	if args.install:
		output_path = install_path

	if not os.path.exists(output_path):
		os.makedirs(output_path)

	neither = not (args.light or args.dark)
	settings = Settings(
		output_path = output_path,
		preview = args.preview,
		default_irc_colours = args.default_irc_colours,
		light = args.light or neither,
		dark = args.dark or neither,
	)

	if args.scheme:
		scheme = os.path.expanduser(args.scheme)
		if not os.path.exists(scheme):
			fatal("No such file: '%s'" % scheme)
		generateTextualStyles(scheme, settings)
	else:
		iterateFiles(config_path, generateTextualStyles, settings)

copyright_txt = """\
Scheme: {title}
Author: {author}

This style was automatically generated by an advanced base16-builder written by
FroZnShiva (https://github.com/FroZnShiva)

This style is based on the Simplified Light style shipped with Textual.

Simplified Light original copyright:

This style is a modified and stripped down version of
the "Simplified" theme developed by "Cowboy" Ben Alman
(http://benalman.com/). Copyright © 2010, 2011, 2012.
"""

design_css = """\
/**
 * {title}
 * @author: {author}
 */

/* @group Basic Body Structure */

* {{
	margin: 0;
	padding: 0;
	font-size: 100%;
	word-wrap: break-word;
}}

body {{
	color: #{base00};
	height: 100%;
	z-index: 100;
	font-size: 12px;
	overflow: hidden;
	overflow-y: visible;
	background-color: #{base07};
}}

#body_home {{
	left: 0;
	right: 0;
	bottom: 0;
	width: 100%;
	z-index: 100;

	position: absolute;
	opacity: 0; /* Set by JavaScript */
	-webkit-transition: opacity 0.8s linear;
}}

body[viewtype=channel] div#body_home {{
	max-height: 96.5%;
}}

.line {{
	padding: 2px 5px 2px 5px;
	clear: both;
}}

.sender {{
	cursor: pointer;
	font-weight: 700;
}}

body[dir=rtl] .sender {{
	display: inline-block;
}}

/* @end */

/* @group Misc */

#loading_screen {{
	position: absolute;
	top: 50%;
	left: 50%;
	margin-top: -11px;
	margin-left: -150px;
	width: 300px;
	height: 21px;
	font-size: 18px;
	background: #{base06};
	border: 1px solid #{base05};
	border-radius: 5px;
	padding: 5px;
	padding-left: 10px;
	opacity: 1; /* Set by JavaScript */
	-webkit-transition: opacity 0.8s linear;
	text-align: center;
}}

.encryptionLock img {{
	float: right;
	margin: 0;
	padding: 0;
	height: 11px;
	margin-top: 2px;
	padding-left: 10px;
}}

/* @end */

/* @group Time */

.time {{
	color: #{base04};
	white-space: nowrap;
}}

body[dir=rtl] .time {{
	padding-left: 0.4em;
	display: inline-block;
}}

/* @end */

/* @group Links */

a {{
	color: #{base0D};
	border-color: #{base0D};
	text-decoration: none;
	border-bottom: dotted 1px;
}}

a:hover {{
	color: #{base0E};
	border-color: #{base0E};
}}

/* @end */

/* @group Topic Bar */

#topic_bar {{
	top: 0;
	left: 0;
	right: 0;
	z-index: 400;
	opacity: 0; /* Set by JavaScript */
	color: #{base02};
	position: fixed;
	padding: 2px 0.5em 3px;
	background-color: rgba({base05r}, {base05g}, {base05b}, 0.95);
	-webkit-transition: opacity 0.8s linear;
	-webkit-font-smoothing: subpixel-antialiased;
	overflow: hidden;
	white-space: nowrap;
	text-overflow: ellipsis;
}}

/* Topic bar hover additions contributed with permission from the project:
 * https://github.com/hbang/Simplified-Light-Modifications
 */

#topic_bar:hover {{
	overflow: visible;
	white-space: normal;
}}

/* @end */

/* @group Images */

.inlineImageCell {{
	overflow: auto;
	display: block;
	margin-top: 5px;
	margin-bottom: 2px;
}}

.inlineImageCell .image {{
	display: inline-block;
	float: left;
	margin-right: 15px;
	margin-left: 10px;
	min-width: 40px;
	max-width: 90%;
}}

.inlineImageCell .closeButton {{
	cursor: pointer;
	border-radius: 5px;
	border: 2px solid #{base05};
	color: #{base02};
	display: inline-block;
	line-height: 14px;
	font-size: 15px;
	font-family: "Helvetica Neue" !important;
	text-indent: 7px;
	width: 16px;
	height: 16px;
	float: left;
	padding-right: 7px;
	padding-left: 0px;
}}

html[systemversion^="10.9"] .inlineImageCell .closeButton,
html[systemversion^="10.8"] .inlineImageCell .closeButton {{
	line-height: 13px;
}}

/* @end */

/* @group Separating History */

div[id=mark] {{
	clear: both;
	position: relative;
	z-index: 295;
	margin-top: -1px;
	border-bottom: 1px dashed;
	border-color: #{base08};
	-webkit-transition: 0.2s linear;
}}

.historic {{
	opacity: 0.5;
}}

/* @end */

/* @group NOTICE / CTCP / WALLOPS */

.line[ltype*=ctcp],
.line[ltype*=notice],
.line[ltype*=wallops] {{
	color: #{base0A};
	z-index: 191;
	background-color: rgba({base0Ar}, {base0Ag}, {base0Ab}, 0.1);
	position: relative;
}}

/* @end */

/* @group Selected User */

.line[ltype*=privmsg]:not(.selectedUser),
.line[ltype*=action]:not(.selectedUser) {{
	transition: background-color 0.5s;
}}

.line.selectedUser[highlight=false] {{
	transition: background-color 0.5s;
	z-index: 190;
	position: relative;
	background-color: rgba({base09r}, {base09g}, {base09b}, 0.1);
}}

/* @end */

/* @group PRIVMSG */

.line[ltype*=privmsg][highlight=true],
.line[ltype*=action][highlight=true] {{
	z-index: 191;
	position: relative;
	font-weight: normal;
	background-color: rgba({base08r}, {base08g}, {base08b}, 0.1);
}}

div[ltype*=privmsg] .sender {{
	white-space: pre-wrap;
}}

/* @end */

/* @group ACTION */

div[ltype*=action] .sender:before {{
	content: "•";
}}

body[dir=ltr] div[ltype*=action] .sender:before {{
	margin-right: 0.4em;
}}

body[dir=rtl] div[ltype*=action] .sender:before {{
	margin-left: 0.4em;
}}

div[ltype*=action] .sender:after {{
	content: "";
}}

/* @end */

/* @group DEBUG / INVITE */

.line[ltype*=invite],
.line[ltype*=debug],
.line[ltype*=rawhtml],
.line[ltype*=dccfiletransfer] {{
	color: #{base02};
	z-index: 190;
	background-color: #{base06};
	position: relative;
}}

/* @end */

/* @group Message of the Day (MOTD)
 *
 * 720, 721, 722 are used by ShadowIRCd for Oper MOTD.
 * 372, 375, 376 are normal MOTD shared by several IRCds.
 */

.line[command="372"],
.line[command="721"] {{
	padding-top: 3px;
	padding-bottom: 3px;
}}

.line[command="375"],
.line[command="720"] {{ /* Start. */
	padding-top: 2px;
	padding-bottom: 3px;
}}

.line[command="376"],
.line[command="722"] {{ /* End. */
	padding-top: 3px;
	padding-bottom: 3px;
}}

.line[command="372"] .message,
.line[command="375"] .message,
.line[command="376"] .message
.line[command="720"] .message,
.line[command="721"] .message,
.line[command="722"] .message {{
	/* font-family: "EspressoMono-Regular", "Menlo" !important; */
}}

/* @end */

/* @group General Events */

.line[ltype*=join],
.line[ltype*=part],
.line[ltype*=quit],
.line[ltype*=nick],
.line[ltype*=mode],
.line[ltype*=topic],
.line[ltype*=website] {{
	color: #{base04};
	background-color: rgba({base06r}, {base06g}, {base06b}, 0.1);
}}

/* Slightly more interesting events */
.line[ltype*=kick],
.line[ltype*=kill],
.line[ltype*=mode][command=mode] {{
	color: #{base02};
	background-color: rgba({base06r}, {base06g}, {base06b}, 0.1);
}}

/* @group Event Indicators */

div[ltype*=join] .message:before {{
	content: "→";
	color: #{base0B};
}}

div[ltype*=kick] .message:before,
div[ltype*=part] .message:before,
div[ltype*=quit] .message:before {{
	content: "←";
	color: #{base08};
}}

div[ltype*=nick] .message:before {{
	content:"◦";
	color: #{base0C};
}}

/* @end */

/* @end */

/* @group Own Messages */

.sender[mtype*=myself] {{
	color: #{base0D};
}}

div[mtype*=myself] {{
	background-color: rgba({base0Dr}, {base0Dg}, {base0Db}, 0.1);
}}

/* @end */

/* @group Nickname Colors */

/* Leave out #{base0D}, it's the color of the own nick */

.sender[mtype*=normal][colornumber='0'],
.inline_nickname[colornumber='0'] {{
	color: #{base08};
}}

.sender[mtype*=normal][colornumber='1'],
.inline_nickname[colornumber='1'] {{
	color: #{base09};
}}

.sender[mtype*=normal][colornumber='2'],
.inline_nickname[colornumber='2'] {{
	color: #{base0A};
}}

.sender[mtype*=normal][colornumber='3'],
.inline_nickname[colornumber='3'] {{
	color: #{base0B};
}}

.sender[mtype*=normal][colornumber='4'],
.inline_nickname[colornumber='4'] {{
	color: #{base0C};
}}

.sender[mtype*=normal][colornumber='5'],
.inline_nickname[colornumber='5'] {{
	color: #{base0E};
}}

.sender[mtype*=normal][colornumber='6'],
.inline_nickname[colornumber='6'] {{
	color: #{base0F};
}}

/* Shuffle RGB values to get some more colors which are similar / harmonic */

/* Swap R <-> B */

.sender[mtype*=normal][colornumber='7'],
.inline_nickname[colornumber='7'] {{
	color: rgb({base08b}, {base08g}, {base08r});
}}

.sender[mtype*=normal][colornumber='8'],
.inline_nickname[colornumber='8'] {{
	color: rgb({base09b}, {base09g}, {base09r});
}}

.sender[mtype*=normal][colornumber='9'],
.inline_nickname[colornumber='9'] {{
	color: rgb({base0Ab}, {base0Ag}, {base0Ar});
}}

.sender[mtype*=normal][colornumber='10'],
.inline_nickname[colornumber='10'] {{
	color: rgb({base0Bb}, {base0Bg}, {base0Br});
}}

.sender[mtype*=normal][colornumber='11'],
.inline_nickname[colornumber='11'] {{
	color: rgb({base0Cb}, {base0Cg}, {base0Cr});
}}

.sender[mtype*=normal][colornumber='12'],
.inline_nickname[colornumber='12'] {{
	color: rgb({base0Db}, {base0Dg}, {base0Dr});
}}

.sender[mtype*=normal][colornumber='13'],
.inline_nickname[colornumber='13'] {{
	color: rgb({base0Eb}, {base0Eg}, {base0Er});
}}

.sender[mtype*=normal][colornumber='14'],
.inline_nickname[colornumber='14'] {{
	color: rgb({base0Fr}, {base0Fg}, {base0Fb});
}}

/* Swap R <-> G */

.sender[mtype*=normal][colornumber='15'],
.inline_nickname[colornumber='15'] {{
	color: rgb({base08g}, {base08r}, {base08b});
}}

.sender[mtype*=normal][colornumber='16'],
.inline_nickname[colornumber='16'] {{
	color: rgb({base09g}, {base09r}, {base09b});
}}

/* This, barely readable */
.sender[mtype*=normal][colornumber='17'],
.inline_nickname[colornumber='17'] {{
	color: rgb({base0Ag}, {base0Ar}, {base0Ab});
}}

.sender[mtype*=normal][colornumber='18'],
.inline_nickname[colornumber='18'] {{
	color: rgb({base0Bg}, {base0Br}, {base0Bb});
}}

.sender[mtype*=normal][colornumber='19'],
.inline_nickname[colornumber='19'] {{
	color: rgb({base0Cg}, {base0Cr}, {base0Cb});
}}

.sender[mtype*=normal][colornumber='20'],
.inline_nickname[colornumber='20'] {{
	color: rgb({base0Dg}, {base0Dr}, {base0Db});
}}

.sender[mtype*=normal][colornumber='21'],
.inline_nickname[colornumber='21'] {{
	color: rgb({base0Eg}, {base0Er}, {base0Eb});
}}

.sender[mtype*=normal][colornumber='22'],
.inline_nickname[colornumber='22'] {{
	color: rgb({base0Fg}, {base0Fr}, {base0Fb});
}}

/* Swap G <-> B */

.sender[mtype*=normal][colornumber='23'],
.inline_nickname[colornumber='23'] {{
	color: rgb({base08r}, {base08b}, {base08g});
}}

.sender[mtype*=normal][colornumber='24'],
.inline_nickname[colornumber='24'] {{
	color: rgb({base09r}, {base09b}, {base09g});
}}

.sender[mtype*=normal][colornumber='25'],
.inline_nickname[colornumber='25'] {{
	color: rgb({base0Ar}, {base0Ab}, {base0Ag});
}}

.sender[mtype*=normal][colornumber='26'],
.inline_nickname[colornumber='26'] {{
	color: rgb({base0Br}, {base0Bb}, {base0Bg});
}}

.sender[mtype*=normal][colornumber='27'],
.inline_nickname[colornumber='27'] {{
	color: rgb({base0Cr}, {base0Cb}, {base0Cg});
}}

.sender[mtype*=normal][colornumber='28'],
.inline_nickname[colornumber='28'] {{
	color: rgb({base0Dr}, {base0Db}, {base0Dg});
}}

.sender[mtype*=normal][colornumber='29'],
.inline_nickname[colornumber='29'] {{
	color: rgb({base0Er}, {base0Eb}, {base0Eg});
}}

.sender[mtype*=normal][colornumber='30'],
.inline_nickname[colornumber='30'] {{
	color: rgb({base0Fr}, {base0Fb}, {base0Fg});
}}

/* @end */
"""

irc_colours_css = """
/* @group Foreground Colors */
.effect[color-number='0']  {{ color: #{base07fixed}   !important; }} /* White       */
.effect[color-number='1']  {{ color: #{base00fixed}   !important; }} /* Black       */
.effect[color-number='2']  {{ color: #{base0D}   !important; }} /* Blue        */
.effect[color-number='3']  {{ color: #{base0B}   !important; }} /* Green       */
.effect[color-number='4']  {{ color: rgba({base08r}, {base08g}, {base08b}, 0.8) !important; }} /* Light Red   */
.effect[color-number='5']  {{ color: #{base0F}   !important; }} /* Brown       */
.effect[color-number='6']  {{ color: #{base0E}   !important; }} /* Purple      */
.effect[color-number='7']  {{ color: #{base09}   !important; }} /* Orange      */
.effect[color-number='8']  {{ color: #{base0A}   !important; }} /* Yellow      */
.effect[color-number='9']  {{ color: rgba({base0Br}, {base0Bg}, {base0Bb}, 0.8) !important; }} /* Light Green */
.effect[color-number='10'] {{ color: #{base0C}   !important; }} /* Cyan        */
.effect[color-number='11'] {{ color: rgba({base0Cr}, {base0Cg}, {base0Cb}, 0.8) !important; }} /* Light Cyan  */
.effect[color-number='12'] {{ color: rgba({base0Dr}, {base0Dg}, {base0Db}, 0.8) !important; }} /* Light Blue  */
.effect[color-number='13'] {{ color: rgba({base0Er}, {base0Eg}, {base0Eb}, 0.8) !important; }} /* Pink        */
.effect[color-number='14'] {{ color: #{base02fixed}   !important; }} /* Gray        */
.effect[color-number='15'] {{ color: #{base05fixed}   !important; }} /* Light Gray  */
/* @end */

/* @group Background Colors */
.effect[bgcolor-number='0']  {{ background-color: #{base07fixed}   !important;}} /* White       */
.effect[bgcolor-number='1']  {{ background-color: #{base00fixed}   !important;}} /* Black       */
.effect[bgcolor-number='2']  {{ background-color: #{base0D}   !important;}} /* Blue        */
.effect[bgcolor-number='3']  {{ background-color: #{base0B}   !important;}} /* Green       */
.effect[bgcolor-number='4']  {{ background-color: rgba({base08r}, {base08g}, {base08b}, 0.8) !important;}} /* Light Red   */
.effect[bgcolor-number='5']  {{ background-color: #{base0F}   !important;}} /* Brown       */
.effect[bgcolor-number='6']  {{ background-color: #{base0E}   !important;}} /* Purple      */
.effect[bgcolor-number='7']  {{ background-color: #{base09}   !important;}} /* Orange      */
.effect[bgcolor-number='8']  {{ background-color: #{base0A}   !important;}} /* Yellow      */
.effect[bgcolor-number='9']  {{ background-color: rgba({base0Br}, {base0Bg}, {base0Bb}, 0.8) !important;}} /* Light Green */
.effect[bgcolor-number='10'] {{ background-color: #{base0C}   !important;}} /* Cyan        */
.effect[bgcolor-number='11'] {{ background-color: rgba({base0Cr}, {base0Cg}, {base0Cb}, 0.8) !important;}} /* Light Cyan  */
.effect[bgcolor-number='12'] {{ background-color: rgba({base0Dr}, {base0Dg}, {base0Db}, 0.8) !important;}} /* Light Blue  */
.effect[bgcolor-number='13'] {{ background-color: rgba({base0Er}, {base0Eg}, {base0Eb}, 0.8) !important;}} /* Pink        */
.effect[bgcolor-number='14'] {{ background-color: #{base02fixed}   !important;}} /* Gray        */
.effect[bgcolor-number='15'] {{ background-color: #{base05fixed}   !important;}} /* Light Gray  */
/* @end */
"""

stylesettings_plist = """\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>Nickname Format</key>
	<string></string>
	<key>Timestamp Format</key>
	<string></string>
	<key>Override Channel Font</key>
	<dict>
		<key>Font Name</key>
		<string></string>
		<key>Font Size</key>
		<integer>0</integer>
	</dict>
	<key>Indentation Offset</key>
	<integer>6</integer>
	<key>Underlying Window Color</key>
	<string>#{base07}</string>
	<key>Force Invert Sidebars</key>
	<false/>
	<key>Template Engine Versions</key>
	<dict>
		<key>default</key>
		<integer>3</integer>
	</dict>
</dict>
</plist>
"""

preview_html = """\
<html viewtype="channel" dir="ltr">
<head>
	<title>{title}</title>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<link rel="stylesheet" type="text/css" href="design.css">
	<style type="text/css">
		html, body, body[type], body {{
			font-family: 'Menlo';
			font-size: 9pt;
		}}
		body div#body_home p {{
			margin-left: 78.24609375px;
			text-indent: -78.24609375px;
		}}
		body .time {{
			width: 78.24609375px;
		}}
		/* Print actions. */
		@media print {{
			#topic_bar {{
				display: none;
			}}
		}}
		/* Reserved lines. */
		body div.line[command="-101"] .message {{
			font-family: "Menlo" !important;
		}}
	</style>
</head>
<body viewtype="channel" dir="ltr">
	<div id="loading_screen" style="opacity: 0; display: none;">View is Loading…</div>
	<div id="body_home" style="opacity: 1;">
		<div ltype="join" command="join" class="line event"><p>
            <span class="time">[17:14:42]  </span>
            <span class="message" ltype="join"><b>FroZnShiva</b> (user.example.com) joined the channel</span>
        </p></div>
		<div ltype="mode" command="mode" class="line event"><p>
            <span class="time">[17:14:42]  </span>
            <span class="message" ltype="mode"><b>irc.example.com</b> sets mode <b>+ntR</b></span>
        </p></div>
		<div ltype="mode" command="324" class="line event"><p>
            <span class="time">[17:14:42]  </span>
            <span class="message" ltype="mode">Mode is <b>+Rnt</b></span>
        </p></div>
		<div ltype="join" command="join" class="line event"><p>
            <span class="time">[17:14:53]  </span>
            <span class="message" ltype="join"><b>Chatter</b> (user.example.com) joined the channel</span>
        </p></div>
		<div ltype="kick" command="kick" class="line event"><p>
            <span class="time">[17:15:04]  </span>
            <span class="message" ltype="kick"><b>FroZnShiva</b> kicked <b>Chatter</b> from the channel (Lorem Ipsum)</span>
        </p></div>
		<div ltype="mode" command="mode" class="line event"><p>
            <span class="time">[17:15:12]  </span>
            <span class="message" ltype="mode"><b>FroZnShiva</b> sets mode <b>+i</b></span>
        </p></div>
		<div ltype="notice" command="notice" highlight="false" class="line text"><p>
            <span class="time">[17:15:19]  </span>
            <span class="message" ltype="notice"><span class="senderContainer"><span class="sender" mtype="normal" nickname="irc.example.com" colornumber="-1">-irc.example.com-</span></span>
            <span class="innerMessage">[Knock] by Chatter!user.example.com (no reason specified)</span></span>
        </p></div>
		<div ltype="mode" command="mode" class="line event"><p>
            <span class="time">[17:16:12]  </span>
            <span class="message" ltype="mode"><b>FroZnShiva</b> sets mode <b>-i</b></span>
        </p></div>
		<div ltype="join" command="join" class="line event"><p>
            <span class="time">[17:16:18]  </span>
            <span class="message" ltype="join"><b>Chatter</b> (user.example.com) joined the channel</span>
        </p></div>
		<div ltype="privmsg" command="privmsg" highlight="false" class="line text"><p>
            <span class="time">[17:16:21]  </span>
            <span class="message" ltype="privmsg"><span class="senderContainer"><span class="sender" mtype="normal" nickname="Chatter" colornumber="12">&lt;Chatter&gt;</span></span>
            <span class="innerMessage">Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</span></span>
        </p></div>
		<div ltype="privmsg" command="privmsg" highlight="false" class="line text"><p>
            <span class="time">[17:16:57]  </span>
            <span class="message" ltype="privmsg"><span class="senderContainer"><span class="sender" mtype="normal" nickname="Chatter" colornumber="12">&lt;Chatter&gt;</span></span>
            <span class="innerMessage">Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo.</span></span>
        </p></div>
		<div ltype="privmsg" mtype="myself" command="privmsg" highlight="false" class="line text"><p>
            <span class="time">[17:17:11]  </span>
            <span class="message" ltype="privmsg"><span class="senderContainer"><span class="sender" mtype="myself" nickname="FroZnShiva" colornumber="2">&lt;@FroZnShiva&gt;</span></span>
            <span class="innerMessage">Quis autem vel eum iure reprehenderit qui in ea voluptate velit esse quam nihil molestiae consequatur, vel illum qui dolorem eum fugiat quo voluptas nulla pariatur?</span></span>
        </p></div>
		<div id="mark"></div>
		<div ltype="privmsg" command="privmsg" highlight="false" class="line text"><p>
            <span class="time">[17:17:36]  </span>
            <span class="message" ltype="privmsg"><span class="senderContainer"><span class="sender" mtype="normal" nickname="Chatter" colornumber="12">&lt;Chatter&gt;</span></span>
            <span class="innerMessage">Ut enim ad minima veniam, quis nostrum exercitationem ullam corporis suscipitlaboriosam, nisi ut aliquid ex ea commodi consequatur? laboriosam, nisi ut aliquid ex ea commodi consequatur?</span></span>
        </p></div>
		<div ltype="privmsg" command="privmsg" highlight="true" class="line text"><p>
            <span class="time">[17:17:53]  </span>
            <span class="message" ltype="privmsg"><span class="senderContainer"><span class="sender" mtype="normal" nickname="Chatter" colornumber="12">&lt;Chatter&gt;</span></span>
            <span class="innerMessage">FroZnShiva: Et harum quidem rerum facilis est et expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio cumque nihil impedit quo minus id quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellendus.</span></span>
        </p></div>
	</div>
	<div id="topic_bar" style="opacity: 0.95;">(No Topic)</div>
</body>
</html>
"""

if __name__ == '__main__': main()
