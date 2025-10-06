# validation.py

import pandas as pd
import sys

def run_pandas_validation():
    """
    Performs a simple, canonical workflow with Pandas to validate its core functionality.
    """
    try:
        # 1. Load a standard, public dataset from a URL.
        # This tests network access and CSV parsing.
        url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
        df = pd.read_csv(url)

        # 2. Perform a non-trivial groupby and aggregation.
        # This tests core data manipulation logic (split-apply-combine).
        age_by_class = df.groupby('Pclass')['Age'].mean()

        # 3. Perform a merge operation.
        # This tests another key feature involving multiple DataFrames.
        df_ages = pd.DataFrame({'Pclass': age_by_class.index, 'MeanAge': age_by_class.values})
        merged_df = pd.merge(df, df_ages, on='Pclass')

        # 4. Perform a validation check on the result.
        # This ensures the operations produced a sane, non-empty result.
        assert not merged_df.empty, "DataFrame became empty after operations."
        assert 'MeanAge' in merged_df.columns, "Merge operation failed to add the new column."
        
        # 5. If all checks pass, print a success metric to stdout and exit cleanly.
        # The agent's `validate_changes` function will parse this output.
        print(f"Validation Passed: Final DataFrame shape {merged_df.shape}")
        sys.exit(0)

    except Exception as e:
        # 6. If any part of the workflow fails, print the error to stderr and exit with a non-zero code.
        print(f"Validation FAILED during Pandas workflow: {type(e).__name__} - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_pandas_validation()