
#***********************************************************************************************************
#*************************** WELCOME MESSAGE ****************************************************************
#***********************************************************************************************************

def minido():
#  pip install mlxtend pandas openpyxl
#  pip install pandas scikit-learn openpyxl matplotlib
  print("**********************************************************")
  print("minido")
  print()
  print()
  print("Function: mc")
  print("Input file format: MS Excel")
  print("Monte Carlo Simulation with minido")
  # print()
  # print()
  print("**********************************************************")


#SUBPACKAGE: minido---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

#***********************************************************************************************************
def minido():
  print("Welcome to use minido for Monte Carlo simulation")
  print("print type mc to call the function")

#SUBPACKAGE: mc ---------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------

#***********************************************************************************************************
def mc():
  import pandas as pd
  import numpy as np
  import matplotlib.pyplot as plt
  from google.colab import files
  import io
  from ipywidgets import widgets, VBox, Button
  import IPython.display as display

  # Upload and read the Excel file
  uploaded = files.upload()
  filename = next(iter(uploaded))
  data = pd.read_excel(io.BytesIO(uploaded[filename]))

  # Define function for Monte Carlo simulation
  def monte_carlo_simulation(data, value_column, periods_to_forecast, num_simulations):
      last_value = data[value_column].iloc[-1]
      returns = data[value_column].pct_change().dropna()
      results = []
      
      for _ in range(num_simulations):
          simulated_values = [last_value]
          for _ in range(periods_to_forecast):
              random_return = np.random.choice(returns)
              simulated_values.append(simulated_values[-1] * (1 + random_return))
          results.append(simulated_values)
      
      results_df = pd.DataFrame(results).T
      return results_df

  # Define function to plot results and create Excel output
  def plot_results_and_output_excel(results_df, value_column, num_simulations, periods_to_forecast):
      display.display(display.HTML(f"<h3 style='font-weight:bold'>Simulation Summary</h3>"))
      display.display(display.HTML(f"<div><strong>Selected Column:</strong> {value_column}</div>"))
      display.display(display.HTML(f"<div><strong>Number of Simulations:</strong> {num_simulations}</div>"))
      display.display(display.HTML(f"<div><strong>Forecast Periods:</strong> {periods_to_forecast}</div>"))
      display.display(display.HTML("<hr>"))  # Horizontal line for separation

      plt.figure(figsize=(10, 6))
      # Compute percentiles for shading
      percentiles = results_df.quantile([0.05, 0.25, 0.75, 0.95], axis=1)
      plt.fill_between(results_df.index, percentiles.loc[0.05], percentiles.loc[0.95], color='lightgrey', label='5th to 95th Percentile')
      plt.fill_between(results_df.index, percentiles.loc[0.25], percentiles.loc[0.75], color='darkgrey', label='25th to 75th Percentile')
      
      plt.plot(results_df.median(axis=1), 'b-', linewidth=2, label='Median Forecast')
      plt.title('Monte Carlo Simulation Results')
      plt.xlabel('Periods')
      plt.ylabel('Forecasted Value')
      plt.legend()
      plt.show()
      
      # Display distribution of outcomes and confidence interval
      final_values = results_df.iloc[-1]
      plt.figure(figsize=(10, 6))
      plt.hist(final_values, bins=30, alpha=0.75, color='skyblue')
      plt.title('Distribution of Final Forecasted Values')
      plt.axvline(final_values.quantile(0.25), color='orange', linestyle='dashed', linewidth=2, label='25th Percentile')
      plt.axvline(final_values.quantile(0.75), color='purple', linestyle='dashed', linewidth=2, label='75th Percentile')
      plt.axvline(final_values.quantile(0.05), color='red', linestyle='dashed', linewidth=2, label='5th Percentile')
      plt.axvline(final_values.quantile(0.95), color='green', linestyle='dashed', linewidth=2, label='95th Percentile')
      plt.axvline(final_values.median(), color='blue', linestyle='solid', linewidth=2, label='Median Value')
      plt.legend()
      plt.show()

      # Display results in a table
      summary_data = {
          'Metric': ['5th Percentile', '25th Percentile', 'Median', '75th Percentile', '95th Percentile'],
          'Value': [
              final_values.quantile(0.05),
              final_values.quantile(0.25),
              final_values.median(),
              final_values.quantile(0.75),
              final_values.quantile(0.95)
          ]
      }
      summary_df = pd.DataFrame(summary_data)
      print(summary_df.to_string(index=False))

      # Output results to an Excel file
      median_values = results_df.median(axis=1)
      forecast_df = pd.DataFrame({
          'Forecast Period': median_values.index,
          'Simulated Value (Median)': median_values.values
      })
      forecast_df.to_excel('monte_carlo_forecast_results.xlsx', index=False)
      print("Excel file with forecast results has been created.")
      files.download('monte_carlo_forecast_results.xlsx')  # Prompt download

  # Interactive function to get user inputs and run simulation
  def interactive_monte_carlo():
      column_label = widgets.Label("Select the column for item value:")
      column = widgets.Dropdown(options=data.columns)
      num_simulations_label = widgets.Label("Enter the number of simulations:")
      num_simulations = widgets.IntText(value=1000)
      periods_to_forecast_label = widgets.Label("Enter the number of periods to forecast:")
      periods_to_forecast = widgets.IntText(value=10)
      run_button = widgets.Button(description="Run Simulation")

      def on_button_clicked(b):
          results_df = monte_carlo_simulation(data, column.value, periods_to_forecast.value, num_simulations.value)
          plot_results_and_output_excel(results_df, column.value, num_simulations.value, periods_to_forecast.value)

      run_button.on_click(on_button_clicked)
      input_widgets = VBox([
          column_label, column,
          num_simulations_label, num_simulations,
          periods_to_forecast_label, periods_to_forecast,
          run_button
      ])
      display.display(input_widgets)

  # Call the interactive function
  interactive_monte_carlo()


