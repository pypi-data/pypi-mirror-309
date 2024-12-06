from typing import Optional, Tuple, List
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re


def get_counts(df):
    pattern = r"_\d+$"  # Matches any suffix starting with "_" followed by digits
    base_peptide_names = list(set([col.rsplit('_', 1)[0] for col in df.columns if col.endswith(('_1', '_2', '_3'))]))
    base_peptide_names = list(set([re.sub(pattern, '', col) for col in df.columns if re.search(pattern, col)]))
    for base_name in base_peptide_names:
        replicate_columns = [col for col in df.columns if re.match(f"{re.escape(base_name)}_\\d+$", col)]
        df[f"{base_name}_count"] = df[replicate_columns].notna().sum(axis=1)
    return df

def make_manhattan_plot(
    df: pd.DataFrame, 
    peptide_name: str, 
    ax = None,
    figsize: Optional[Tuple[int, int]] = (12, 6),
    show: bool = True,
    highlighted_compounds: Optional[List[str]] = None,
    save_path: str =None,
    gene: str = None,
    xticks: bool=True,
    cutoff: float=None
) -> None:
    """
    Create a Manhattan-style plot of relative abundance for a given peptide,
    with the option to highlight specific compounds.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'Compound' column and columns for
                       mean and standard deviation of specified peptide.
    peptide_name (str): Name of the peptide for which to plot abundance.
    ax (Optional[plt.Axes]): Matplotlib Axes to plot on. If None, creates a new
                             figure.
    figsize (Optional[Tuple[int, int]]): Figure size if ax is None. Defaults to
                                         (12, 6).
    show (bool): Whether to show the plot if created. Defaults to True.
    highlighted_compounds (Optional[List[str]]): List of compounds to highlight
                                                 with a distinct color and marker.

    Returns:
    None
    """
    mean_column = f'{peptide_name}_mean'
    std_column = f'{peptide_name}_std'
    count_column = f'{peptide_name}_count'  # Add a count column if available
    
    # Step 1: Sort by mean values
    df_sorted = df.sort_values(by=mean_column)

    # Replace any `pandas.NA` with `np.nan` in mean and std columns
    df_sorted[mean_column] = df_sorted[mean_column].astype('float')
    df_sorted[std_column] = df_sorted[std_column].astype('float')
    df_sorted[mean_column] = df_sorted[mean_column].replace(pd.NA, np.nan)
    df_sorted[std_column] = df_sorted[std_column].replace(pd.NA, np.nan)

    
    # Calculate standard error if count data is available
    if count_column in df.columns:
        df_sorted['SE'] = df_sorted[std_column] / np.sqrt(df_sorted[count_column])
    else:
        raise ValueError(f"Column '{count_column}' with counts is required for SE calculation.")

    # Get compounds with relative abundance below threshold if one is provided
    if cutoff is not None:
        df_sorted = df_sorted.loc[df_sorted[mean_column]<cutoff]

    # Step 2: Plot mean values with error bars for standard error
    create_new_fig = False
    if ax is None:
        create_new_fig = True
        fig, ax = plt.subplots(figsize=figsize)
    
    # Plot all compounds
    ax.errorbar(
        df_sorted["Compound"],         
        df_sorted[mean_column],        
        yerr=df_sorted["SE"],          # Use standard error for yerr
        fmt='o',                       
        capsize=4,                     
        color="blue",                  # Default color for non-highlighted
        label=peptide_name             
    )

    # Highlight specific compounds if provided
    if highlighted_compounds:
        highlight_df = (
            df_sorted[df_sorted["Compound"].isin(highlighted_compounds)]
        )
        
        ax.errorbar(
            highlight_df["Compound"],         
            highlight_df[mean_column],        
            yerr=highlight_df["SE"],          # Use standard error for highlighted compounds
            capsize=4,
            fmt="o",
            color="orange",                 # Color for highlighted compounds
            label=f"{peptide_name} (Highlighted)"
        )
    
    ax.axhline(1, color="red", linestyle="--")
    
    # Step 3: Customize the plot
    ax.set_xlabel("Compound")
    ax.set_ylabel("Relative Abundance (log2)")

    if gene is None:
        title = f"Relative Abundance for {peptide_name} by Compound"
    else:
        title = f"Relative Abundance for {gene}: {peptide_name} by Compound"
    ax.set_title(title)
    plt.xticks(rotation=45)   
    plt.tight_layout()   
    ax.set_yscale('log', base=2)
    # ax.set_ylim((2**-5, 2**5))

    if not xticks:
        for tick in ax.get_xticklabels():
            if tick.get_text() not in highlighted_compounds:
                tick.set_visible(False)

    if save_path is not None:
        plt.savefig(save_path)
    
    # Show plot only if a new figure was created
    if create_new_fig and show:
        plt.show()



def plot_compound_peptide_abundance(
    df: pd.DataFrame, 
    compounds: List[str], 
    peptide_names: List[str],
    highlighted_peptides: Optional[List[str]] = None,
    figsize: Optional[Tuple[int, int]] = (8,4),  # Adjusted for vertical layout
    save_path: Optional[str] = None,
    show: bool = True
) -> None:
    """
    Create a plot for each compound, showing relative abundance across multiple peptides,
    with the option to highlight specific peptides. Peptides are displayed on the y-axis.

    Parameters:
    df (pd.DataFrame): DataFrame containing 'Compound' column and columns for mean and 
                       standard deviation of specified peptides.
    compounds (List[str]): List of compounds for which to create plots.
    peptide_names (List[str]): List of peptide names to plot for each compound.
    highlighted_peptides (Optional[List[str]]): List of peptides to highlight with a distinct color.
    figsize (Optional[Tuple[int, int]]): Size of each figure. Defaults to (8, 10) for vertical layout.
    save_path (Optional[str]): Path to save each plot image with compound name in the filename.
    show (bool): Whether to show the plot if created. Defaults to True.

    Returns:
    None
    """
    for compound in compounds:
        # Filter data for the specific compound
        compound_data = df[df["Compound"] == compound]
        
        if compound_data.empty:
            print(f"No data found for compound {compound}. Skipping plot.")
            continue

        # Create lists for y (peptides) and x (abundance) values
        means = [compound_data[f"{peptide}_mean"].values[0] 
                 for peptide in peptide_names]
        stds = [compound_data[f"{peptide}_std"].values[0]
                for peptide in peptide_names]

        # Create a new figure and axis
        fig, ax = plt.subplots(figsize=figsize)
        
        # Plot all peptides for the compound, with peptides on the y-axis
        ax.errorbar(
            means,
            peptide_names,
            xerr=stds,
            fmt='o',
            capsize=4,
            color="blue",
            label="Peptides"
        )

        # Highlight specific peptides if provided
        if highlighted_peptides:
            highlighted_means = [
                means[i] for i, peptide in enumerate(peptide_names)
                if peptide in highlighted_peptides
            ]
            highlighted_stds = [
                stds[i] for i, peptide in enumerate(peptide_names) 
                if peptide in highlighted_peptides
            ]
            highlighted_peptides_y = [
                peptide for peptide in peptide_names 
                if peptide in highlighted_peptides
            ]
            ax.errorbar(
                highlighted_means,
                highlighted_peptides_y,
                xerr=highlighted_stds,
                fmt='o',
                color="orange",
                label="Highlighted Peptides"
            )

        ax.axvline(1, color="red", linestyle="--")
        
        # Customize plot
        ax.set_ylabel("Peptide")
        ax.set_xlabel("Relative Abundance")
        ax.set_title(f"Relative Abundance for Compound {compound} by Peptide")
        plt.tight_layout()

        # Save plot if save path is provided
        if save_path is not None:
            plt.savefig(f"{save_path}/{compound}_abundance.png")
        
        # Show plot only if desired
        if show:
            plt.show()
        else:
            plt.close(fig)  # Close plot if not showing