/* Defined in: "Textual 5.app -> Contents -> Resources -> JavaScript -> API -> core.js" */

var mappedSelectedUsers = new Array();
var groupCount = 0;
var currentChannel = undefined;

Textual.viewInitiated = function(viewType, serverHash, channelHash, channelName)
{
	currentChannel = (viewType == 'channel') ? channelName : undefined
}

Textual.viewBodyDidLoad = function()
{
	Textual.fadeOutLoadingScreen(1.00, 0.95);

	setTimeout(function() {
		Textual.scrollToBottomOfView()
	}, 500);
}

Textual.newMessagePostedToView = function(line)
{
	var element = document.getElementById("line-" + line);

	updateNicknameAssociatedWithNewMessage(element);

	if (enableGrouping && currentChannel) {
		if (groupingInclude) {
			enableGrouping = groupingInclude.indexOf(currentChannel) != -1;
		} else if (groupingExclude) {
			enableGrouping = groupingExclude.indexOf(currentChannel) == -1;
		}
	}

	if (enableGrouping) {
		groupGeneralUserEvents(element);
	}
}

Textual.nicknameSingleClicked = function(e)
{
	userNicknameSingleClickEvent(e);
}

function updateNicknameAssociatedWithNewMessage(e)
{
	/* We only want to target plain text messages. */
	var elementType = e.getAttribute("ltype");

	if (elementType == "privmsg" || elementType == "action") {
		/* Get the nickname information. */
		var senderSelector = e.querySelector(".sender");

		if (senderSelector) {
			/* Is this a mapped user? */
			var nickname = senderSelector.getAttribute("nickname");

			/* If mapped, toggle status on for new message. */
			if (mappedSelectedUsers.indexOf(nickname) > -1) {
				toggleSelectionStatusForNicknameInsideElement(senderSelector);
			}
		}
	}
}

function toggleSelectionStatusForNicknameInsideElement(e)
{
	/* e is nested as the .sender so we have to go three parents
	 up in order to reach the parent div that owns it. */
	var parentSelector = e.parentNode.parentNode.parentNode.parentNode;

	parentSelector.classList.toggle("selectedUser");
}

function userNicknameSingleClickEvent(e)
{
	/* This is called when the .sender is clicked. */
	var nickname = e.getAttribute("nickname");

	/* Toggle mapped status for nickname. */
	var mappedIndex = mappedSelectedUsers.indexOf(nickname);

	if (mappedIndex == -1) {
		mappedSelectedUsers.push(nickname);
	} else {
		mappedSelectedUsers.splice(mappedIndex, 1);
	}

	/* Gather basic information. */
	var documentBody = document.getElementById("body_home");

	var allLines = documentBody.querySelectorAll('div[ltype="privmsg"], div[ltype="action"]');

	/* Update all elements of the DOM matching conditions. */
	for (var i = 0, len = allLines.length; i < len; i++) {
		var sender = allLines[i].querySelectorAll(".sender");

		if (sender.length > 0) {
			if (sender[0].getAttribute("nickname") === nickname) {
				toggleSelectionStatusForNicknameInsideElement(sender[0]);
			}
		}
	}
}

function isGeneralUserEvent(element)
{
	var type = element.getAttribute("command");
	return ["join", "part", "quit", "nick"].indexOf(type) != -1;
}

function isGroup(element)
{
	var type = element.getAttribute("ltype");
	return type == "group";
}

function isMarker(element)
{
	return element && element.id && element.id == 'mark';
}

function groupGeneralUserEvents(currentLine)
{
	var previousLine = currentLine.previousElementSibling;

	// Ignore marker line
	if (isMarker(previousLine))
		previousLine = previousLine.previousElementSibling;

	if (!isGeneralUserEvent(currentLine) || !previousLine)
		return;

	var previousType = previousLine.getAttribute("ltype");

	// Don't group if there is just one line.
	if (!(isGeneralUserEvent(previousLine) || isGroup(previousLine)))
		return;

	var group = previousLine;

	if (!isGroup(previousLine) && previousType != "general_user_events") {
		group = createGroup("general_user_events");
		currentLine.parentElement.insertBefore(group, currentLine);
	}

	if (!isGroup(previousLine)) {
		increaseAttribute(group, previousType + "s");
		addLineToGroup(group, previousLine);
	}

	// Increase before decorating, else the numbers might be off.
	var currentType = currentLine.getAttribute("command");
	increaseAttribute(group, currentType + "s");

	addLineToGroup(group, currentLine);
}

function createGroup(name)
{
	var group = document.createElement("details");
	group.id = "group-" + groupCount;
	group.setAttribute("ltype", "group");
	group.setAttribute("class", "line group");
	group.setAttribute("gtype", name);

	if (expandNewGroups) {
		group.setAttribute("open", "");
	}

	var head = document.createElement("summary");
	head.id = "group_head-" + groupCount;
	group.appendChild(head);

	var body = document.createElement("div");
	body.id = "group_body-" + groupCount;
	body.setAttribute("class", "group_body");
	group.appendChild(body);

	var time = document.createElement("span");
	time.setAttribute("class", "time");
	head.appendChild(time);

	var message = document.createElement("span");
	message.setAttribute("class", "message");
	message.appendChild(document.createTextNode(""));
	head.appendChild(message);

	groupCount++;

	return group;
}

function addLineToGroup(group, line)
{
	line.parentNode.removeChild(line);
	group.lastElementChild.appendChild(line);

	var head = group.firstElementChild;
	var time = line.firstElementChild.firstElementChild.cloneNode(true);

	head.removeChild(head.firstElementChild);
	head.insertBefore(time, head.firstElementChild);

	decorateGroup(group)
}

function increaseAttribute(element, name)
{
	var value = Number(element.getAttribute(name));
	element.setAttribute(name, value + 1);
}

function decorateGroup(group)
{
	function stringifyValue(name, title)
	{
		if (title == undefined)
			title = name

		var value = Number(group.getAttribute(name + "s"));
		return value + " " + (value == 1 ? title : title + "s");
	}

	var gtype = group.getAttribute("gtype");
	var head = group.firstElementChild;
	var message = head.lastElementChild;
	var text = message.firstChild;

	if (gtype == "general_user_events") {
		text.textContent = " " +
			stringifyValue("join") + ", " +
			stringifyValue("part") + ", " +
			stringifyValue("quit") + " and " +
			stringifyValue("nick", "nick change");
	}
}
