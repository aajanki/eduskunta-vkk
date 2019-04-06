import json
import sys
import pandas as pd


def main():
    data = json.load(sys.stdin)
    df = pd.DataFrame(data)

    print(f'Total documents: {df.shape[0]}')
    print()
    print(df.groupby('position')
          .size()
          .sort_values(ascending=False)
          .to_string())
    print()
    print(df.tags
          .apply(pd.Series)
          .stack()
          .reset_index(level=1, drop=True)
          .to_frame('tag')
          .reset_index()
          .groupby('tag')
          .size()
          .sort_values(ascending=False)
          .head(100)
          .to_string())
    
    

if __name__ == '__main__':
    main()
