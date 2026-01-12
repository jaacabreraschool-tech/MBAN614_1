import pandas as pd

# Load Summary tab
summary_df = pd.read_excel("HR Cleaned Data 01.09.26.xlsx", sheet_name="Summary")

# Print column names to debug
print("Columns in Summary tab:", summary_df.columns)

# If you see something like "Net Talent Gain/Loss", use that
net_df = summary_df[["Year", "Net Change"]].copy()
net_df.rename(columns={"Net Change": "NetChange"}, inplace=True)

# Assign status
net_df["Status"] = net_df["NetChange"].apply(
    lambda x: "Increase" if x > 0 else ("Decrease" if x < 0 else "No Change")
)

# Debug print
print(net_df[["Year", "NetChange", "Status"]])
