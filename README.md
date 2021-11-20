<h1 align="center">Welcome to PinkMartini! 🍸</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Language-Python-brightgreen" />
  <img src="https://img.shields.io/pypi/pyversions/latest" />
  <img src="https://img.shields.io/badge/Contributers-1-red" />
</p>

<p align="center">
  <img src="https://github.com/vsharma8363/PinkMartini/blob/main/image.png?raw=true" />
</p>

## Table of Contents 🗂

  * [Description](#description)<br/>
  * [Prerequisites](#prereqs)<br/>
  * [Installation](#installation)<br/>
  * [Running](#running)<br/>
  * [Contact](#contact)<br/>

## <a name="description"></a>Description 📝

Discord application written in Python allowing for Youtube playback and generic URL audio in a server. Queues not enabled... yet.

## <a name="prereqs"></a>Prerequisites 💻

Before you begin, ensure you have met the following requirements:<br/>
✅ &nbsp; You have `Python 3+` installed on your machine <br/>
✅ &nbsp; You have setup a Discord bot using the administrator interface <a src="https://discord.com/developers/applications">here</a> <br/>
✅ &nbsp; You have created a Discord bot and saved the unique token <br/>

**Note:** Do not, under any circumstance, post your Discord bot token on GitHub or otherwise, keep that key private at all costs!

## <a name="installation"></a>Installation 📥

Install the required libraries (and be sure to install pip3 if you haven't already).

```
pip3 install discord;
pip3 install requests;
pip3 install youtube_dl;
```

## <a name="running"></a>Running 🚀

Go to this line in pinkmartini.py and replace 'SUPER SECRET TOKEN GOES HERE' with your token generated earlier.

```
client.run('SUPER SECRET TOKEN GOES HERE')
```

Then all you have to do is run using the following command:

```
python3 pinkmartini.py
```

Add the bot to any server using the invite URL: ```https://discord.com/api/oauth2/authorize?client_id=APPLICATION_ID_HERE&permissions=0&scope=bot%20applications.commands```.

### Tips & Functionality 💡

PinkMartini supports the following
- ```!play``` examples:
  - ```!play https://www.youtube.com/watch?v=XfR9iY5y94s``` (Youtube URL)
  - ```!play http://stream.radioparadise.com/rock-128``` (Generic Audio URL/Online Radio)
  - ```!play Yesterday-Beatles``` (Search query)
- ```!pause``` (Pauses current audio)
- ```!stop``` (Clears the audio player)
- ```!leave``` (If for some reason you want the bot to leave the channel)

##  <a name="contact"></a>Contact 📫
For any questions, please contact [@vsharma8363](https://github.com/vsharma8363)
