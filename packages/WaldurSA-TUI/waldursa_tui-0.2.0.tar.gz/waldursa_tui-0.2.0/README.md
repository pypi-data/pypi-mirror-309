## Waldur Site Agent TUI
Waldur Site Agent TUI is a terminal user interface (TUI) for Waldur Site Agent.

## How to use
In order to analyze the code you can view it in the public GitHub repository. Another option is to clone it into your machine for example, but be advised that the use will be limited for the lack of data. <br>
To use the TUI, you would need a test environment with simulated data. We have set up a virtual machine for that. We also need your ssh key to give you access to the machine, you can email one of us for that. There you have two options, you can use already pulled source code and installed dependencies or you could try doing it yourself.

### Using TUI in the Test VM with everything set up and installed:
  - ssh into ubuntu@193.40.155.199
  - Go to ```cd development/Waldur``` if you want to use already pulled code
  - Run the TUI with ```poetry run python src/WaldurSA_TUI/main.py```


### Using TUI in the Test VM and setting everything up yourself:
  - ssh into ubuntu@193.40.155.199
  - Go to a review directory if you want to test pulling source code yourself
    - ```cd review/mentor``` if you are the mentor
    - ```cd review/peer``` if you are the peer reviewer
    - Clone the GitHub project and move into it with ``cd WaldurSA-TUI`` <br>
  - To run it from the source code, you'd need to install the following:
    - Install Poetry https://python-poetry.org/docs/#installing-with-pipx
    - Install libsystemd-dev ```sudo apt install libsystemd-dev```
    - In the cloned project install Poetry dependencies with ```poetry install```
    - Run the TUI with ```poetry run python src/WaldurSA_TUI/main.py```

### UI
- You can use either a mouse or a keyboard to navigate
- To switch between TUI elements
  - Press ‘tab’
- To switch to a different tab
  - Select the tab switcher
  - Press ‘left arrow’ or ‘right arrow’ to switch tabs
- To navigate between dates or tables
  - Use the arrow keys


### For developers
From PyPi:
- To install the PyPi package use the following command:
  - ``pip install WaldurSA-TUI``
  - or a specific version, for example: ``pip install WaldurSA-TUI==0.2.0``
  - To run the package use the following command: ``waldur_site_agent_tui``


## Release notes
### Release notes 0.2.0
Logs tab:
- Real log usage
  - The TUI now uses logs realated to the Waldur Site agent
- Logs are now refreshed automatically
  - Refresh every 30 seconds, which can be paused
- Filtering
  - Added Sort by Date
    - From, to, and from - to sorting
  - Added Sort by timeframe
    - From, to, and from - to sorting
  - Added Sort alphabetically
    - Sort from A-Z
- Optimizations
  - loading in logs does not freeze the TUI

Configured offerings tab
- Real configured offerings usage
  - The TUI now uses configured offerings realated to the Waldur Site agent

Dashboard
- Real data usage
  - The TUI now fetches services from waldur the Waldur Site agent

Known bugs
- Logs tab
  - 'Clear filters' button deletes all visiable data
  - Filters do not take affect on new logs
  - When scrolling down in a table with keyboard doesn't show active row on screen
- Some automated test fail
  - Likely related to how async and threads are implemented in the configured offerings file. Random failing hasn't happened with log testing.
  - Should not impact manual testing
- Fixed
  - Filtering and async mismatch
    - Filters did not work correctly with async at first


### Release notes 0.1.0
- Added dashboard tab
  - Only includes static test info for now
- Added logs tab
  - Includes 3 log categories
  - Logs are searchable
  - UI for search by date is added
    - Not yet functional
  - A simple export logs button
    - Export logs that can be viewed
    - May need to change the functionality in the future
  - Table for log info
    - Only includes test logs for now
- Added configured offerings tab
  - Offerings are searchable
  - A list view for available offerings
  - Each offering has a view for its included items and values
  - Only includes test info for now
- Added keybindings
  - ‘q’ for quitting the TUI
  - ‘e’ for a simulated error popup
- Known Bugs
  - None, works with test data
