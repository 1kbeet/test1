from shroomdk import ShroomDK 
import streamlit as st
import pandas as pd
st.write("NFTx $PUNK Price")

# Initialize `ShroomDK` with your API Key
sdk = ShroomDK(st.secrets["FLIPSIDE_API_KEY"])

# Parameters can be passed into SQL statements 
# via native string interpolation
sql = f"""
   with punkin as (
  select 
  block_timestamp,
  amount_out_usd / (amount_in / pow(10,18)) as usd_per_punk,
  amount_out / (amount_in / pow(10,18)) as weth_per_punk
  from ethereum.core.ez_dex_swaps
  where (
   token_in = lower('0x269616D549D7e8Eaa82DFb17028d0B212D11232A') -- PUNK token
   and token_out = lower('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2') -- WETH
  )
),
punkout as (
  select 
  block_timestamp,
  amount_in_usd / (amount_out / pow(10,18)) as usd_per_punk,
  amount_in / (amount_out / pow(10,18)) as weth_per_punk
  from ethereum.core.ez_dex_swaps
  where (
   token_out = lower('0x269616D549D7e8Eaa82DFb17028d0B212D11232A')-- PUNK token
   and token_in = lower('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2') -- WETH
  )
)
select * from punkin
UNION
select * from punkout order by block_timestamp desc ;
"""

# Run the query against Flipside's query engine 
# and await the results
query_result_set = sdk.query(sql)
df = pd.DataFrame(query_result_set.records)
st.write(df)
st.line_chart(data=df, x="block_timestamp", y="weth_per_punk", width=0, height=0, use_container_width=True)
# Iterate over the results
for record in query_result_set.records:
    block_timestamp = record['block_timestamp']
    weth_per_punk = record['weth_per_punk']
    usd_per_punk = record['usd_per_punk']
    print(f"{block_timestamp},{weth_per_punk}ETH, ${usd_per_punk}")
