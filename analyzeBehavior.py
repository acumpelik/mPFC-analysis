import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import the data
JC240_data = pd.read_csv("JC240_data.csv")
JC241_data = pd.read_csv("JC241_data.csv")

# Explore the data
JC240_data.head() # show data = sanity check
# JC240_data.info() # Index, data type, and memory information

#%%
# Split the data by Session ID
sessionID_JC240 = JC240_data["Session_ID"].unique() # returns an array of unique session IDs
numSessions_JC240 = len(sessionID_JC240) # returns the number of sessions
numTrials_JC240 = JC240_data.groupby("Session_ID").size() # lists the number of trials per session

sessionID_JC241 = JC241_data["Session_ID"].unique()
numSessions_JC241 = len(sessionID_JC241)
numTrials_JC241 = JC241_data.groupby("Session_ID").size()

#%%
# Calculate correct trials
correctTrials_JC240 = np.zeros((1, numSessions_JC240))
for idx in range(1, numSessions_JC240+1):
    session = JC240_data.loc[JC240_data.Session_ID==idx]
    correctTrials_JC240[0,idx-1] = sum(session.CorrectBool)

correctTrials_JC241 = np.zeros((1, numSessions_JC241))
for idx in range(1, numSessions_JC241+1):
    session = JC241_data.loc[JC241_data.Session_ID==idx]
    correctTrials_JC241[0,idx-1] = sum(session.CorrectBool)

# Calculate accuracy
accuracy_JC240 = (correctTrials_JC240/numTrials_JC240.values)*100 # session accuracy (percent)
accuracy_JC241 = (correctTrials_JC241/numTrials_JC241.values)*100

#%%
# # Plot both animals
# JC240_plot = plt.plot(sessionID_JC240, accuracy_JC240[0,:], 'cornflowerblue', label="JC240")
# JC241_plot = plt.plot(sessionID_JC241, accuracy_JC241[0,:], 'r', label="JC241")
# plt.axvline(9, color='cornflowerblue', linestyle=":", linewidth="1.3")
# plt.axvline(13, color='red', linestyle=":", linewidth="1.3")
# plt.xticks(np.arange(0, numSessions_JC240+1, step=1))
# plt.xlabel('Session number')
# plt.ylabel('Accuracy (%)')
# plt.title('Performance JC240 and JC241')
# plt.legend()
# plt.axis([1,16,0,100])
# plt.show()
# # plt.savefig("Performance-schema.png", dpi=500)

#%%
# Plot JC240
JC240_plot = plt.plot(sessionID_JC240, accuracy_JC240[0,:], 'cornflowerblue')
plt.axvline(9, color='cornflowerblue', linestyle="--", linewidth="1.3", label='schema start')
plt.axhline(85, color='lightgray', linestyle=":", linewidth="1.3")
plt.xticks(np.arange(0, numSessions_JC240+1, step=1))
plt.xlabel('Session number')
plt.ylabel('Accuracy (%)')
plt.title('Performance JC240')
plt.legend(loc="upper left")
plt.axis([1,16,0,100])
plt.show()
# plt.savefig("Performance-JC240.png", dpi=500)

# Plot JC241
JC241_plot = plt.plot(sessionID_JC241, accuracy_JC241[0,:], 'r')
plt.axvline(13, color='red', linestyle="--", linewidth="1.3", label="schema start")
plt.axhline(85, color='lightgray', linestyle=":", linewidth="1.3")
plt.xticks(np.arange(0, numSessions_JC241+1, step=1))
plt.xlabel('Session number')
plt.ylabel('Accuracy (%)')
plt.title('Performance JC240')
plt.legend()
plt.axis([1,15,0,100])
plt.show()
# plt.savefig("Performance-JC241.png", dpi=500)

#%%
# calculate accuracy for each flavor separately, by session
# formula: correct trials with flavor / total trials with flavor
# step 1: calculate total trials with flavor per session
# step 2: calculate correct trials with flavor per session

trialsBySession = JC240_data.groupby("Session_ID")
flavors_JC240 = trialsBySession.groupby("Flavor").size() # returns the number of trials per session, grouped by flavor



















































