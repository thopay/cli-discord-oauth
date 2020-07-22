# cli-discord-oauth

Creates a temporary flask server for discord authentication. Easily changeable to return user details, servers, and connections. Default setup is to check to see if a user is a member of a specific server. Returns an object containing user details and whether they are authorized or not. Originally designed for Mist #0069.
# Example

With no changes to the script besides the sever ID to check for, here's what's returned for different cases.

## User logs in and is authenticated

![enter image description here](https://i.gyazo.com/5a08a192743d003979af762ffe9922c9.png)

## User logs in but is not authenticated

![enter image description here](https://i.gyazo.com/67be89bdc4678b685293eb360aee4a6f.png)

## User does not login in time

![enter image description here](https://i.gyazo.com/b55c61d6122899f44b960f181947fb10.png)

