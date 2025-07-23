1. File Handling Module (file class):
   - Reads personnel list from `name_list.txt` (supports Chinese encoding)
   - Cleans data: Removes newline characters and leading/trailing double quotes from each line
   - Processes numeric input: Uses keyboard input to select the number of people to draw (1-6)

2. Random Selection Algorithm:
   - Uses `random.sample()` to ensure non-repetitive selection
   - Dynamic list management: Selected names are removed from the current list
   - List reset mechanism: Automatically reloads original list when remaining names are insufficient

3. User Interaction System:
   - Spacebar controls selection state (start/stop)
   - Number keys 1-9 select number of people to draw
   - Enter key confirms selection
   - Backspace key resets number selection

4. Visual Interface:
   - Background image display
   - Layered text rendering: Top prompts, middle name display, bottom operation guidance
   - Name grouping: Displays names in two lines when exceeding 3 names

5. Auxiliary Functions:
   - Background music control (pause/resume)
   - Operation logging: Saves selected names with UTC timestamps to `log.txt`
   - Input validation: Limits selection count (1-6 people) with error prompts

Workflow:
1. Initialize background image and music
2. Phase 1: Input selection count using number keys (1-6 people)
3. Phase 2: Press spacebar to start random selection
4. Display selected names
5. Press spacebar again to confirm, record log and update list
6. Repeat for new selections


This program is suitable for scenarios requiring random selection like classroom Q&A or prize draws, featuring a clean, user-friendly interface with intuitive operation logic.
