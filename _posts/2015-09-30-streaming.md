---
layout: post
title:  Server->Client streaming using Server-Sent Events (SSE)
date:   2015-09-30 03:30:00
tags:
- html
- js
- python
---

In the previous tutorial we covered using query strings to send arguments to the server to specify options or parameters for how a function should run. While passing such arguments is super useful, this communication is very limited. It can only happen at the time when the request is sent, and can only go one way, from the client to the server. What if we needed to send information back from the server, at any time, even when a process was running? In our case this would be very useful for monitoring the activity of the backend server, particularly as we begin to develop more advanced processing code that could take some time to execute. In these cases it would be great if the server could communicate back to the client about which stage of the process it was on, and how much longer the process is expected to take. 

In the past, sending information back from the server involved a large amount of setup, and used complicated technologies such as [WebSocket](https://en.wikipedia.org/wiki/WebSocket) to handle the communication. More recently, a new technology called [Server-Sent Events](https://en.wikipedia.org/wiki/Server-sent_events) (SSE) has been developed to simplify such communication within smaller applications. SSE allows the server to send back information using simple HTTP requests, which can be picked up by the client's web browser and presented back to the user. Most modern browsers support SSE, as does Flask, so we will use it to develop a communications channel from our server to the client to get real time feedback on the processes being run.

Switch to the `04-streaming` branch in the ['week-4’](https://github.com/data-mining-the-city/week-4) repository.




http://flask.pocoo.org/snippets/116/