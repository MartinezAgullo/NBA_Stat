import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit

#######
# main
#######
def main():
    csv_file = 'nba_player_salaries.csv'
    print("Reading: "+str(csv_file))
    df = pd.read_csv(csv_file, index_col='Ranking')
    #plot_histogram(df,30)
    #get_average_by_pos(df)
    starters_df = TeamStarters(df)
    TeamBudget(starters_df)


########
#  TeamBudget: Plots the budget of each team and the salary differences
########
def TeamBudget(starters_df):
    print("TeamBudget ::  Calculating the budget of each team and comparying the salaries of the highest and lowest payed athletes in each team.")
    teams = starters_df['Team'].unique()
    TeamBudget = []
    economy = []
    for team in teams:
        squad = starters_df[starters_df['Team']==team]
        #print(squad)
        squad_budget = squad['Salary'].sum()
        squad_max_pay = squad['Salary'].max()
        squad_min_pay = squad['Salary'].min()
        scale_dif = squad_max_pay/squad_min_pay
        #print(scale_dif)
        economy.append({'Team':team, 'Budget': squad_budget, 'Max/Min scale': scale_dif})
    
    economy_df = pd.DataFrame(economy)
    #print(economy_df)

    fig, ax1 = plt.subplots(figsize=(14, 8))
    # Plot the 'Budget' as a bar plot
    teams = economy_df['Team']
    budgets = economy_df['Budget']
    ax1.bar(teams, budgets, color='blue', label='Budget', alpha=0.6)

    # Label each bar with the corresponding team name
    for i, (team, budget) in enumerate(zip(teams, budgets)):
        #ax1.text(i, budget, team, ha='center', va='bottom', rotation='vertical', fontsize=8)
        pass
    ax1.set_xlabel('Team')
    ax1.set_ylabel('Budget', color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax1.tick_params(axis='x', rotation=90)  # Rotate x-axis labels to show them vertically
    ax1.set_xticks(range(len(teams)))  # Ensure there's a tick for each team
    ax1.set_xticklabels(teams, rotation='vertical')  # Set the tick labels as team names

    # Create the second Y-axis to plot the 'Max/Min scale'
    ax2 = ax1.twinx()
    max_min_scale = economy_df['Max/Min scale']
    ax2.plot(teams, max_min_scale, color='red', label='Max/Min Scale', marker='o', linestyle='None')
    ax2.set_ylabel('Max/Min Scale', color='red')
    ax2.tick_params(axis='y', labelcolor='red')

    # Adding legends
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('NBA Team Economy Analysis')
    plt.tight_layout()  # Adjust the layout to make room for the rotated x-axis labels
    plt.show()


        

########
#  TeamStarters: Single player per position and team.
########
def TeamStarters(dataframe):
    print("TeamStarters: Defines the starting lineup of each team according to the salary of the athletes and using one player per posstion")
    #return dataframe.groupby(['Team', 'Position']).apply(lambda x: x.nlargest(1, 'Salary')).reset_index(drop=True)
    sorted_df = dataframe.sort_values(by=['Team', 'Position', 'Salary'], ascending=[True, True, False])
    starters_df = sorted_df.drop_duplicates(subset=['Team', 'Position'])
    starters_df.reset_index(drop=True, inplace=True)
    return starters_df


########
#  get_average_by_pos: Average salary by position.
#  This is calculated with the top 70 of each pos.
########
def get_average_by_pos(dataframe):
    sample_size
    print("get_average_by_pos: Salary per position averaged over the top "+str(sample_size)+" players on that possition.")
    #top_salaries_by_position = dataframe.groupby('Position').apply(lambda x: x.nlargest(min(len(x), sample_size), 'Salary')).reset_index(drop=True)
    #averages = top_salaries_by_position.groupby('Position')['Salary'].mean().reset_index(name='Average Salary')

    positions = dataframe['Position'].unique()
    averages = []
    for pos in positions:
        df_filtered = dataframe[dataframe['Position'] == pos]
        df_sorted = df_filtered.sort_values(by='Salary', ascending=False) 
        top_salaries = df_sorted.head(min(70, len(df_sorted))) #Top players each category
        avg_salary = top_salaries['Salary'].mean() / 1_000_000
        averages.append({'Position': pos, 'Average Salary (Millions)': avg_salary})
    averages_df = pd.DataFrame(averages)
    print(averages_df)
    return averages_df



########
#  plot_histogram: Distribution of salaries and fit the histo
########
def plot_histogram(df, n_bins):
    print("plot_histogram: Draws a histogram displaying the salary distribution and performs a fit.")
    convert = False
    dolar_euro = 0.93
    if convert: 
        print("Convert from $ to €")
        df['Salary'] = df['Salary']*dolar_euro

    counts, bin_edges = np.histogram(df['Salary'], bins=n_bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:])/2

    print("Use curve_fit to find the best fitting parameters")
    # Bounds for ABCD ::   A + B**(C*x+D)
    lower_bounds = [-20, 0.1, 1, -5]
    upper_bounds = [+20, 0.9, 10, +5]

    params, covariance = curve_fit(model, bin_centers, counts, p0=[0.1, 0.4, 1.1, 0])
    print(params)

    # Plot the histogram
    plt.figure(figsize=(10, 6))
    plt.hist(df['Salary'], bins=n_bins, color='blue', edgecolor='black', label='Data')

    # Plot the fitting curve
    x_fit = np.linspace(bin_edges[0], bin_edges[-1], 1000)
    y_fit = model(x_fit, *params)
    plt.plot(x_fit, y_fit, color='red', linewidth=2, label='Fit: A + B^(C*x + D)')

    plt.title('Distribution of NBA Player Salaries with Fitting Curve')
    if convert: plt.xlabel('Salary (€)')
    else: plt.xlabel('Salary ($)')
    plt.ylabel('Number of Players')
    plt.xticks(rotation=45)
    plt.legend()
    plt.show()
    
    print("end")


# Define function to fit
def model(x, A, B, C, D):
    return A + B**(C*x+D)


main()