**User:**

<task>
“Design a customer retention and churn prediction dashboard page that identifies at-risk customers, displays churn probability metrics, retention trends, prediction results, and key churn factors using machine learning outputs.”
and 
“Create a business insights page that generates actionable recommendations from customer analytics data. Include revenue insights, retention strategies, customer lifetime value analysis, ROI metrics, and plain-English business recommendations.”
</task>
<environment_details>
# VSCode Visible Files
docs/SEGMENTATION_PLAN_SUMMARY.md

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:55:11.786Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/Users/meetjain/Downloads/InsightStream-main) Files
.gitignore
app.py
LICENSE
README.md
requirements.txt
.streamlit/
data/
data/generate_synthetic_data.py
data/sample_churn.csv
docs/
docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md
docs/DATA_EXPLORATION_ARCHITECTURE.md
docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md
docs/IMPLEMENTATION_GUIDE.md
docs/PLAN_SUMMARY.md
docs/SCALABLE_ARCHITECTURE.md
docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md
docs/SEGMENTATION_PLAN_SUMMARY.md
docs/SEGMENTATION_TECHNICAL_GUIDE.md
models/
models/encoders_scalers/
models/encoders_scalers/num_scaler.pkl
models/encoders_scalers/ohe_encoder.pkl
notebooks/
notebooks/eda_playground.ipynb
pages/
pages/1_Data_Exploration.py
pages/2_Customer_Groups.py
pages/3_Customer_Retention.py
pages/4_Business_Insights.py
src/
src/biz_metrics.py
src/data_prep.py
src/eda_utils.py
src/helpers.py
src/sql_utils.py
tests/
tests/smoke_tests.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze the current project structure and design comprehensive solutions for both the customer retention/churn prediction dashboard and the business insights page.

<read_file>
<args>
  <file>
    <path>pages/3_Customer_Retention.py</path>
  </file>
  <file>
    <path>pages/4_Business_Insights.py</path>
  </file>
  <file>
    <path>app.py</path>
  </file>
  <file>
    <path>src/biz_metrics.py</path>
  </file>
  <file>
    <path>README.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>pages/3_Customer_Retention.py</path>
<content lines="1-542">
  1 | """
  2 | Why Do Customers Leave? Le# Set page config
  3 | st.set_page_config(
  4 |     page_title="Customer Retention",
  5 |     page_icon=":arrows_counterclockwise:",
  6 |     layout="wide"
  7 | )nd Out!
  8 | 
  9 | This page helps business owners understand why customers are walking away.
 10 | No complicated statistics - just clear insights about what might be driving customers to leave.
 11 | 
 12 | We look at things like:
 13 | - Which customer groups are leaving the most?
 14 | - What behaviors signal that someone might leave soon?
 15 | - How can you spot the warning signs earlier?
 16 | 
 17 | Think of it as your churn detective tool - helping you solve the mystery of the disappearing customers!
 18 | """
 19 | import streamlit as st
 20 | import pandas as pd
 21 | import numpy as np
 22 | import os
 23 | import sys
 24 | from pathlib import Path
 25 | 
 26 | # Add parent directory to path
 27 | sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 28 | 
 29 | # Import utilities
 30 | from src.helpers import (
 31 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL
 32 | )
 33 | from src.data_prep import prepare_data_for_analysis
 34 | from src.sql_utils import run_sql
 35 | 
 36 | # Set page config
 37 | st.set_page_config(
 38 |     page_title="Customer Retention",
 39 |     page_icon="�",
 40 |     layout="wide"
 41 | )
 42 | 
 43 | # Initialize session state if not exists
 44 | if 'data' not in st.session_state:
 45 |     st.session_state.data = None
 46 | if 'data_processed' not in st.session_state:
 47 |     st.session_state.data_processed = False
 48 | 
 49 | # Page title
 50 | st.title("Customer Retention Power Tools!")
 51 | st.markdown("Discover why customers leave and get powerful strategies to keep them coming back!")
 52 | 
 53 | # Check if data is loaded
 54 | if st.session_state.data is None:
 55 |     st.warning("No data loaded. Please load data from the home page.")
 56 |     st.stop()
 57 | 
 58 | # Check if churn column exists
 59 | if TARGET_COL not in st.session_state.data.columns:
 60 |     st.error(f"Churn column '{TARGET_COL}' not found in data. Cannot perform churn analysis.")
 61 |     st.stop()
 62 | 
 63 | # Process data if not already processed
 64 | if not st.session_state.data_processed:
 65 |     with st.spinner("Processing data for analysis..."):
 66 |         df = prepare_data_for_analysis(st.session_state.data)
 67 |         st.session_state.data = df
 68 |         st.session_state.data_processed = True
 69 | else:
 70 |     df = st.session_state.data
 71 | 
 72 | # Create tabs for different churn analysis views
 73 | tab1, tab2, tab3 = st.tabs(["Churn Factors", "Churn Trends", "Correlation Analysis"])
 74 | 
 75 | # Churn Factors Tab
 76 | with tab1:
 77 |     st.header("Key Churn Factors")
 78 |     st.markdown("Analyze which factors have the strongest relationship with customer churn.")
 79 |     
 80 |     # Calculate feature correlations with churn
 81 |     numeric_cols = [col for col in NUMERIC_COLS if col in df.columns]
 82 |     if numeric_cols:
 83 |         # Calculate correlations
 84 |         corr_with_churn = df[numeric_cols + [TARGET_COL]].corr()[TARGET_COL].drop(TARGET_COL).sort_values(ascending=False)
 85 |         
 86 |         # Display correlations
 87 |         st.subheader("Correlation with Churn")
 88 |         
 89 |         # Create correlation dataframe
 90 |         corr_df = pd.DataFrame({
 91 |             'Feature': corr_with_churn.index,
 92 |             'Correlation': corr_with_churn.values
 93 |         })
 94 |         
 95 |         # Create visualization
 96 |         import plotly.express as px
 97 |         
 98 |         fig = px.bar(
 99 |             corr_df,
100 |             x='Correlation',
101 |             y='Feature',
102 |             orientation='h',
103 |             color='Correlation',
104 |             color_continuous_scale='RdBu_r',
105 |             title="Feature Correlations with Churn"
106 |         )
107 | 
108 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
109 | 
110 |         fig.update_layout(height=500)
111 |         st.plotly_chart(fig, use_container_width=True)
112 |         
113 |         # Add insight
114 |         top_pos = corr_df.iloc[0]['Feature']
115 |         top_pos_corr = corr_df.iloc[0]['Correlation']
116 |         top_neg = corr_df.iloc[-1]['Feature']
117 |         top_neg_corr = corr_df.iloc[-1]['Correlation']
118 |         
119 |         st.info(f"""
120 |         Insight: 
121 |         - {top_pos} has the strongest positive correlation with churn ({top_pos_corr:.2f}). Higher values increase churn risk.
122 |         - {top_neg} has the strongest negative correlation with churn ({top_neg_corr:.2f}). Higher values decrease churn risk.
123 |         """)
124 |     
125 |     # Categorical features analysis
126 |     st.subheader("Churn Rate by Categorical Features")
127 |     
128 |     # Select categorical features
129 |     cat_cols = [col for col in CATEGORICAL_COLS + BINARY_COLS if col in df.columns]
130 |     
131 |     if cat_cols:
132 |         # Select feature to analyze
133 |         selected_cat = st.selectbox("Select categorical feature:", cat_cols)
134 |         
135 |         # Calculate churn rate by category
136 |         churn_by_cat = df.groupby(selected_cat)[TARGET_COL].mean() * 100
137 |         counts_by_cat = df.groupby(selected_cat).size()
138 |         
139 |         # Create dataframe
140 |         cat_analysis = pd.DataFrame({
141 |             selected_cat: churn_by_cat.index,
142 |             'Churn Rate (%)': churn_by_cat.values,
143 |             'Count': counts_by_cat.values
144 |         })
145 |         
146 |         # Sort by churn rate
147 |         cat_analysis = cat_analysis.sort_values('Churn Rate (%)', ascending=False)
148 |         
149 |         # Display as table
150 |         st.dataframe(cat_analysis, use_container_width=True)
151 |         
152 |         # Create visualization
153 |         fig = px.bar(
154 |             cat_analysis,
155 |             x=selected_cat,
156 |             y='Churn Rate (%)',
157 |             color='Churn Rate (%)',
158 |             color_continuous_scale=['#4ECDC4', '#FFD166', '#FF6B6B'],
159 |             text=cat_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
160 |             title=f"Churn Rate by {selected_cat}"
161 |         )
162 |         
163 |         fig.update_layout(height=400)
164 |         st.plotly_chart(fig, use_container_width=True)
165 |         
166 |         # Add insight
167 |         highest_cat = cat_analysis.iloc[0][selected_cat]
168 |         highest_rate = cat_analysis.iloc[0]['Churn Rate (%)']
169 |         lowest_cat = cat_analysis.iloc[-1][selected_cat]
170 |         lowest_rate = cat_analysis.iloc[-1]['Churn Rate (%)']
171 |         
172 |         st.info(f"""
173 |         Insight: 
174 |         - {highest_cat} has the highest churn rate at {highest_rate:.1f}%
175 |         - {lowest_cat} has the lowest churn rate at {lowest_rate:.1f}%
176 |         - The difference of {highest_rate - lowest_rate:.1f} percentage points is significant!
177 |         """)
178 |     
179 |     # Numeric feature analysis
180 |     st.subheader("Churn by Numeric Features")
181 |     
182 |     # Select feature to analyze
183 |     if numeric_cols:
184 |         selected_num = st.selectbox("Select numeric feature:", numeric_cols)
185 |         
186 |         # Create visualization
187 |         import plotly.figure_factory as ff
188 |         
189 |         # Create histogram grouped by churn
190 |         churned = df[df[TARGET_COL] == 1][selected_num]
191 |         retained = df[df[TARGET_COL] == 0][selected_num]
192 |         
193 |         hist_data = [retained, churned]
194 |         group_labels = ['Retained', 'Churned']
195 |         colors = ['#4ECDC4', '#FF6B6B']
196 |         
197 |         fig = ff.create_distplot(
198 |             hist_data, 
199 |             group_labels, 
200 |             colors=colors,
201 |             bin_size=(df[selected_num].max() - df[selected_num].min()) / 20,
202 |             show_rug=False
203 |         )
204 |         
205 |         fig.update_layout(
206 |             title=f"Distribution of {selected_num} by Churn Status",
207 |             xaxis_title=selected_num,
208 |             yaxis_title="Density",
209 |             height=400
210 |         )
211 |         
212 |         st.plotly_chart(fig, use_container_width=True)
213 |         
214 |         # Calculate stats
215 |         churned_mean = churned.mean()
216 |         retained_mean = retained.mean()
217 |         diff_pct = abs(churned_mean - retained_mean) / retained_mean * 100
218 |         
219 |         if churned_mean > retained_mean:
220 |             st.info(f"""
221 |             Insight: 
222 |             - Churned customers have {diff_pct:.1f}% higher {selected_num} on average ({churned_mean:.2f} vs {retained_mean:.2f})
223 |             - Customers with higher {selected_num} are more likely to churn
224 |             """)
225 |         else:
226 |             st.info(f"""
227 |             Insight: 
228 |             - Churned customers have {diff_pct:.1f}% lower {selected_num} on average ({churned_mean:.2f} vs {retained_mean:.2f})
229 |             - Customers with lower {selected_num} are more likely to churn
230 |             """)
231 | 
232 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
233 | 
234 | # Churn Trends Tab
235 | with tab2:
236 |     st.header("Churn Trends")
237 |     st.markdown("Analyze churn patterns over different dimensions.")
238 |     
239 |     # Churn by tenure buckets
240 |     if 'tenure_bucket' in df.columns:
241 |         st.subheader("Churn by Customer Tenure")
242 |         
243 |         # Calculate churn rate by tenure
244 |         churn_by_tenure = df.groupby('tenure_bucket')[TARGET_COL].mean() * 100
245 |         counts_by_tenure = df.groupby('tenure_bucket').size()
246 |         
247 |         # Create dataframe
248 |         tenure_analysis = pd.DataFrame({
249 |             'Tenure': churn_by_tenure.index,
250 |             'Churn Rate (%)': churn_by_tenure.values,
251 |             'Count': counts_by_tenure.values
252 |         })
253 |         
254 |         # Sort by bucket order
255 |         bucket_order = ['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
256 |         tenure_analysis['Tenure'] = pd.Categorical(tenure_analysis['Tenure'], categories=bucket_order, ordered=True)
257 |         tenure_analysis = tenure_analysis.sort_values('Tenure')
258 |         
259 |         # Display as table
260 |         st.dataframe(tenure_analysis, use_container_width=True)
261 |         
262 |         # Create visualization
263 |         import plotly.express as px
264 |         
265 |         fig = px.line(
266 |             tenure_analysis,
267 |             x='Tenure',
268 |             y='Churn Rate (%)',
269 |             markers=True,
270 |             text=tenure_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
271 |             title="Churn Rate by Customer Tenure"
272 |         )
273 |         
274 |         fig.update_layout(height=400)
275 |         st.plotly_chart(fig, use_container_width=True)
276 |         
277 |         # Add insight
278 |         highest_tenure = tenure_analysis.loc[tenure_analysis['Churn Rate (%)'].idxmax()]['Tenure']
279 |         highest_rate = tenure_analysis.loc[tenure_analysis['Churn Rate (%)'].idxmax()]['Churn Rate (%)']
280 |         
281 |         st.info(f"""
282 |         Insight: 
283 |         - Customers in the {highest_tenure} tenure bracket have the highest churn rate at {highest_rate:.1f}%
284 |         - This indicates a critical period in the customer lifecycle that needs attention
285 |         """)
286 | 
287 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
288 |     
289 |     # Churn by recency buckets
290 |     if 'recency_bucket' in df.columns:
291 |         st.subheader("Churn by Purchase Recency")
292 |         
293 |         # Calculate churn rate by recency
294 |         churn_by_recency = df.groupby('recency_bucket')[TARGET_COL].mean() * 100
295 |         counts_by_recency = df.groupby('recency_bucket').size()
296 |         
297 |         # Create dataframe
298 |         recency_analysis = pd.DataFrame({
299 |             'Recency': churn_by_recency.index,
300 |             'Churn Rate (%)': churn_by_recency.values,
301 |             'Count': counts_by_recency.values
302 |         })
303 |         
304 |         # Sort by bucket order
305 |         bucket_order = ['0-30 days', '31-60 days', '61-90 days', 'Over 90 days']
306 |         recency_analysis['Recency'] = pd.Categorical(recency_analysis['Recency'], categories=bucket_order, ordered=True)
307 |         recency_analysis = recency_analysis.sort_values('Recency')
308 |         
309 |         # Display as table
310 |         st.dataframe(recency_analysis, use_container_width=True)
311 |         
312 |         # Create visualization
313 |         fig = px.line(
314 |             recency_analysis,
315 |             x='Recency',
316 |             y='Churn Rate (%)',
317 |             markers=True,
318 |             text=recency_analysis['Churn Rate (%)'].round(1).astype(str) + '%',
319 |             title="Churn Rate by Purchase Recency"
320 |         )
321 |         
322 |         fig.update_layout(height=400)
323 |         st.plotly_chart(fig, use_container_width=True)
324 |         
325 |         # Add insight
326 |         highest_recency = recency_analysis.loc[recency_analysis['Churn Rate (%)'].idxmax()]['Recency']
327 |         highest_rate = recency_analysis.loc[recency_analysis['Churn Rate (%)'].idxmax()]['Churn Rate (%)']
328 |         
329 |         st.info(f"""
330 |         Insight: 
331 |         - Customers who haven't purchased in {highest_recency} have the highest churn rate at {highest_rate:.1f}%
332 |         - This indicates a critical window after which customers are much more likely to leave
333 |         """)
334 |     
335 |     # Combination analysis
336 |     st.subheader("Multi-dimensional Churn Analysis")
337 |     
338 |     # Select dimensions
339 |     dimension_options = [col for col in df.columns if col not in [TARGET_COL, ID_COL] and df[col].nunique() < 10]
340 |     
341 |     if len(dimension_options) >= 2:
342 |         col1, col2 = st.columns(2)
343 |         
344 |         with col1:
345 |             dim1 = st.selectbox("Select first dimension:", dimension_options, index=0)
346 |         
347 |         with col2:
348 |             remaining_options = [col for col in dimension_options if col != dim1]
349 |             dim2 = st.selectbox("Select second dimension:", remaining_options, index=0)
350 |         
351 |         # Calculate churn by dimensions
352 |         churn_by_dims = df.groupby([dim1, dim2])[TARGET_COL].mean() * 100
353 |         counts_by_dims = df.groupby([dim1, dim2]).size()
354 |         
355 |         # Create dataframe
356 |         multi_analysis = pd.DataFrame({
357 |             dim1: [x[0] for x in churn_by_dims.index],
358 |             dim2: [x[1] for x in churn_by_dims.index],
359 |             'Churn Rate (%)': churn_by_dims.values,
360 |             'Count': counts_by_dims.values
361 |         })
362 |         
363 |         # Sort by churn rate
364 |         multi_analysis = multi_analysis.sort_values('Churn Rate (%)', ascending=False)
365 |         
366 |         # Display as table
367 |         st.dataframe(multi_analysis, use_container_width=True)
368 |         
369 |         # Create heatmap
370 |         import plotly.graph_objects as go
371 |         
372 |         # Pivot data for heatmap
373 |         heatmap_data = df.groupby([dim1, dim2])[TARGET_COL].mean() * 100
374 |         heatmap_data = heatmap_data.reset_index().pivot(index=dim1, columns=dim2, values=TARGET_COL)
375 |         
376 |         # Create heatmap
377 |         fig = go.Figure(data=go.Heatmap(
378 |             z=heatmap_data.values,
379 |             x=heatmap_data.columns,
380 |             y=heatmap_data.index,
381 |             colorscale='RdBu_r',
382 |             colorbar=dict(title='Churn Rate (%)'),
383 |             text=np.round(heatmap_data.values, 1),
384 |             texttemplate='%{text}%',
385 |             textfont={"size":10}
386 |         ))
387 | 
388 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
389 |         
390 |         fig.update_layout(
391 |             title=f"Churn Rate by {dim1} and {dim2}",
392 |             height=500
393 |         )
394 |         
395 |         st.plotly_chart(fig, use_container_width=True)
396 |         
397 |         # Add insight
398 |         if len(multi_analysis) > 0:
399 |             highest_dim1 = multi_analysis.iloc[0][dim1]
400 |             highest_dim2 = multi_analysis.iloc[0][dim2]
401 |             highest_rate = multi_analysis.iloc[0]['Churn Rate (%)']
402 |             highest_count = multi_analysis.iloc[0]['Count']
403 |             
404 |             lowest_dim1 = multi_analysis.iloc[-1][dim1]
405 |             lowest_dim2 = multi_analysis.iloc[-1][dim2] 
406 |             lowest_rate = multi_analysis.iloc[-1]['Churn Rate (%)']
407 |             lowest_count = multi_analysis.iloc[-1]['Count']
408 |             
409 |             st.info(f"""
410 |             Insight: 
411 |             - The highest churn rate of {highest_rate:.1f}% occurs with {dim1}={highest_dim1} and {dim2}={highest_dim2} (affects {highest_count} customers)
412 |             - The lowest churn rate of {lowest_rate:.1f}% occurs with {dim1}={lowest_dim1} and {dim2}={lowest_dim2} (affects {lowest_count} customers)
413 |             - This combination analysis helps target specific customer segments for retention efforts
414 |             """)
415 | 
416 | # Correlation Analysis Tab
417 | with tab3:
418 |     st.header("Correlation Analysis")
419 |     st.markdown("Analyze relationships between different features and churn.")
420 |     
421 |     # Correlation matrix
422 |     st.subheader("Feature Correlation Matrix")
423 |     
424 |     # Select features for correlation
425 |     numeric_cols = [col for col in df.columns if pd.api.types.is_numeric_dtype(df[col]) and col != ID_COL]
426 |     
427 |     if len(numeric_cols) > 1:
428 |         # Calculate correlation matrix
429 |         corr_matrix = df[numeric_cols].corr()
430 |         
431 |         # Create heatmap
432 |         import plotly.graph_objects as go
433 |         
434 |         fig = go.Figure(data=go.Heatmap(
435 |             z=corr_matrix.values,
436 |             x=corr_matrix.columns,
437 |             y=corr_matrix.index,
438 |             colorscale='RdBu_r',
439 |             colorbar=dict(title='Correlation'),
440 |             text=np.round(corr_matrix.values, 2),
441 |             texttemplate='%{text}',
442 |             textfont={"size":10}
443 |         ))
444 |         
445 |         fig.update_layout(
446 |             title="Feature Correlation Matrix",
447 |             height=600
448 |         )
449 |         
450 |         st.plotly_chart(fig, use_container_width=True)
451 |         
452 |         # Add insight
453 |         if TARGET_COL in corr_matrix.columns:
454 |             churn_corr = corr_matrix[TARGET_COL].drop(TARGET_COL)
455 |             top_pos = churn_corr.nlargest(1).index[0]
456 |             top_pos_corr = churn_corr.nlargest(1).values[0]
457 |             top_neg = churn_corr.nsmallest(1).index[0]
458 |             top_neg_corr = churn_corr.nsmallest(1).values[0]
459 |             
460 |             st.info(f"""
461 |             Insight: 
462 |             - {top_pos} has the strongest positive correlation with churn ({top_pos_corr:.2f})
463 |             - {top_neg} has the strongest negative correlation with churn ({top_neg_corr:.2f})
464 |             - Also note other strong feature correlations which indicate related customer behaviors
465 |             """)
466 |     else:
467 |         st.warning("Not enough numeric columns for correlation analysis.")
468 |     
469 |     # Pairplot for key features
470 |     st.subheader("Pairwise Relationships")
471 |     
472 |     # Select features for pairplot
473 |     if len(numeric_cols) > 2:
474 |         # Let user select top features
475 |         num_features = st.slider("Number of features to include:", min_value=2, max_value=min(5, len(numeric_cols)), value=3)
476 |         
477 |         # Always include churn if available
478 |         if TARGET_COL in numeric_cols:
479 |             selected_features = [TARGET_COL]
480 |             remaining_features = [col for col in numeric_cols if col != TARGET_COL]
481 |         else:
482 |             selected_features = []
483 |             remaining_features = numeric_cols
484 |         
485 |         # If we have correlations with churn, select the most correlated features
486 |         if TARGET_COL in corr_matrix.columns:
487 |             churn_corr = corr_matrix[TARGET_COL].drop(TARGET_COL)
488 |             top_corr_features = churn_corr.abs().nlargest(num_features).index.tolist()
489 |             selected_features.extend([f for f in top_corr_features if f not in selected_features])
490 |         else:
491 |             # Otherwise let user select
492 |             feature_options = [col for col in numeric_cols if col != TARGET_COL]
493 |             user_selected = st.multiselect("Select features to include:", feature_options, default=feature_options[:num_features])
494 |             selected_features.extend([f for f in user_selected if f not in selected_features])
495 |         
496 |         # Ensure we have the right number of features
497 |         selected_features = selected_features[:num_features]
498 | 
499 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
500 |         
501 |         if len(selected_features) > 1:
502 |             # Create scatter plot matrix
503 |             import plotly.express as px
504 |             
505 |             fig = px.scatter_matrix(
506 |                 df,
507 |                 dimensions=selected_features,
508 |                 color=TARGET_COL if TARGET_COL in df.columns else None,
509 |                 color_discrete_map={0: '#4ECDC4', 1: '#FF6B6B'} if TARGET_COL in df.columns else None,
510 |                 title="Feature Relationships"
511 |             )
512 |             
513 |             fig.update_layout(height=600)
514 |             st.plotly_chart(fig, use_container_width=True)
515 |             
516 |             st.info("""
517 |             Tip: 
518 |             - Look for clear separation between red (churned) and teal (retained) points
519 |             - Features with better separation are stronger predictors of churn
520 |             - Clusters indicate customer segments with similar behaviors
521 |             """)
522 |         else:
523 |             st.warning("Please select at least 2 features for the pairwise plot.")
524 |     else:
525 |         st.warning("Not enough numeric columns for pairwise relationship analysis.")
526 | 
527 | # Help section at the bottom
528 | with st.expander("Churn Analysis Tips"):
529 |     st.markdown("""
530 |     **How to Use Churn Analysis:**
531 |     
532 |     1. **Key Factors**: Focus on features with strong correlation to churn (both positive and negative)
533 |     
534 |     2. **Combination Analysis**: Look for specific combinations of factors that have unusually high churn rates
535 |     
536 |     3. **Critical Windows**: Pay attention to time-based patterns like recency and tenure windows with high churn
537 |     
538 |     4. **Leading Indicators**: Features with high correlation to churn can serve as early warning signs
539 |     
540 |     5. **Segment Targeting**: Use the multi-dimensional analysis to identify specific customer segments for 
541 |        targeted retention campaigns
542 |     """)
</content>
</file>
<file><path>pages/4_Business_Insights.py</path>
<content lines="1-344">
  1 | """
  2 | Actionable Advice You Can Ac# Set page config
  3 | st.set_page_config(
  4 |     page_title="Business Insights",
  5 |     page_icon=":bulb:",
  6 |     layout="wide"
  7 | ) Use!
  8 | 
  9 | This is where all the analysis turns into real-world actions you can take.
 10 | No confusing jargon or complicated strategies - just clear, practical recommendations
 11 | that can help keep your customers happy and your business growing.
 12 | 
 13 | We'll help you:
 14 | - Understand what the data is really saying about your customers
 15 | - Figure out which customers need attention right now
 16 | - Calculate the real dollars-and-cents impact of keeping customers around
 17 | - Create simple reports you can share with your team
 18 | 
 19 | It's like having a friendly business consultant in your pocket!
 20 | """
 21 | import streamlit as st
 22 | import pandas as pd
 23 | import numpy as np
 24 | import os
 25 | import sys
 26 | import io
 27 | from pathlib import Path
 28 | 
 29 | # Add parent directory to path
 30 | sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
 31 | 
 32 | # Import utilities
 33 | from src.helpers import (
 34 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL
 35 | )
 36 | from src.data_prep import prepare_data_for_analysis
 37 | 
 38 | # Set page config
 39 | st.set_page_config(
 40 |     page_title="Business Insights",
 41 |     page_icon="�",
 42 |     layout="wide"
 43 | )
 44 | 
 45 | # Initialize session state if not exists
 46 | if 'data' not in st.session_state:
 47 |     st.session_state.data = None
 48 | 
 49 | # Page title and description
 50 | st.title("Business Insights Gold Mine!")
 51 | st.markdown("Transform your customer data into money-making action plans that will revolutionize your business!")
 52 | 
 53 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 54 | 
 55 | 
 56 | # Check if data is loaded
 57 | if st.session_state.data is None:
 58 |     st.warning("No data loaded. Please load data from the home page.")
 59 |     st.stop()
 60 | 
 61 | # Process data if needed
 62 | df = st.session_state.data
 63 | 
 64 | # --- Main Content ---
 65 | col1, col2 = st.columns([1, 1])
 66 | 
 67 | with col1:
 68 |     st.subheader("Key Insights")
 69 |     
 70 |     # Overall churn rate
 71 |     churn_rate = df[TARGET_COL].mean() * 100
 72 |     
 73 |     st.metric("Overall Churn Rate", f"{churn_rate:.1f}%")
 74 |     
 75 |     # Calculate churn rates by segments if available
 76 |     if 'segment' in df.columns:
 77 |         st.write("Churn Rate by Customer Segment:")
 78 |         segment_churn = df.groupby('segment')[TARGET_COL].mean() * 100
 79 |         segment_counts = df.groupby('segment').size()
 80 |         
 81 |         for segment, rate in segment_churn.items():
 82 |             count = segment_counts[segment]
 83 |             st.metric(f"{segment} ({count} customers)", f"{rate:.1f}%")
 84 |     
 85 |     # Top churn factors
 86 |     if len(NUMERIC_COLS) > 0:
 87 |         st.write("Top Churn Indicators:")
 88 |         
 89 |         # Check which numeric columns actually exist in the dataframe
 90 |         available_numeric_cols = [col for col in NUMERIC_COLS if col in df.columns]
 91 |         
 92 |         if available_numeric_cols and TARGET_COL in df.columns:
 93 |             try:
 94 |                 # Calculate correlations with churn
 95 |                 corrs = df[available_numeric_cols + [TARGET_COL]].corr()[TARGET_COL].drop(TARGET_COL)
 96 |                 top_corrs = corrs.abs().sort_values(ascending=False).head(3)
 97 |                 
 98 |                 for feature in top_corrs.index:
 99 |                     correlation = corrs[feature]
100 |                     direction = "increases" if correlation > 0 else "decreases"
101 |                     st.write(f"- Higher **{feature}** {direction} churn risk ({correlation:.2f})")
102 |             except Exception:
103 |                 st.info("Insufficient data to calculate correlation indicators.")
104 |         else:
105 |             st.info("Insufficient columns to calculate churn indicators.")
106 | 
107 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
108 | 
109 | with col2:
110 |     st.subheader("Recommended Actions")
111 |     
112 |     # Basic recommendations based on churn rate
113 |     if churn_rate > 20:
114 |         st.error("Your churn rate is significantly high!")
115 |         st.write("""
116 |         **Immediate actions recommended:**
117 |         1. Implement a customer retention program
118 |         2. Review pricing and value proposition
119 |         3. Improve customer onboarding process
120 |         """)
121 |     elif churn_rate > 10:
122 |         st.warning("Your churn rate is moderately high")
123 |         st.write("""
124 |         **Recommended actions:**
125 |         1. Implement targeted retention offers
126 |         2. Improve customer support response times
127 |         3. Analyze key friction points in customer journey
128 |         """)
129 |     else:
130 |         st.success("Your churn rate is relatively low")
131 |         st.write("""
132 |         **Recommended actions:**
133 |         1. Focus on upselling loyal customers
134 |         2. Implement referral programs
135 |         3. Continue monitoring satisfaction metrics
136 |         """)
137 | 
138 | # Segment-specific recommendations
139 | st.header("Segment-Specific Recommendations")
140 | 
141 | if 'segment' in df.columns:
142 |     # Calculate churn rates and value by segment
143 |     segment_analysis = df.groupby('segment').agg({
144 |         TARGET_COL: 'mean',
145 |         'avg_order_value': 'mean' if 'avg_order_value' in df.columns else lambda x: 0,
146 |         'total_orders': 'mean' if 'total_orders' in df.columns else lambda x: 0,
147 |     }).reset_index()
148 |     
149 |     # Add count column separately
150 |     segment_counts = df.groupby('segment').size().reset_index(name='Count')
151 |     segment_analysis = segment_analysis.merge(segment_counts, on='segment')
152 |     
153 |     segment_analysis.columns = ['Segment', 'Churn Rate', 'Avg Order Value', 'Avg Orders', 'Count']
154 |     segment_analysis['Churn Rate'] = segment_analysis['Churn Rate'] * 100
155 |     
156 |     # Sort by count descending
157 |     segment_analysis = segment_analysis.sort_values('Count', ascending=False)
158 |     
159 |     # Display table
160 |     st.dataframe(segment_analysis)
161 |     
162 |     # Show recommendations for top segment
163 |     if len(segment_analysis) > 0:
164 |         top_segment = segment_analysis.iloc[0]['Segment']
165 |         top_segment_churn = segment_analysis.iloc[0]['Churn Rate']
166 |         
167 |         st.subheader(f"Focus on {top_segment} Segment")
168 |         
169 |         if top_segment_churn > 15:
170 |             st.write(f"""
171 |             This segment has a {top_segment_churn:.1f}% churn rate and represents your largest customer group.
172 |             
173 |             **Recommended retention strategy:**
174 |             1. Conduct satisfaction surveys to identify pain points
175 |             2. Create loyalty rewards specific to this segment's behaviors
176 |             3. Implement proactive outreach before typical churn periods
177 |             """)
178 |         else:
179 |             st.write(f"""
180 |             This segment has a {top_segment_churn:.1f}% churn rate and represents your largest customer group.
181 |             
182 |             **Recommended growth strategy:**
183 |             1. Analyze what's working well for this segment
184 |             2. Find lookalike customers for acquisition
185 |             3. Test upselling and cross-selling opportunities
186 |             """)
187 | else:
188 |     st.info("Customer segmentation not available. Run the Customer Segments analysis to get segment-specific recommendations.")
189 | 
190 | # Action planning section
191 | st.header("Action Planning")
192 | 
193 | col1, col2 = st.columns(2)
194 | 
195 | with col1:
196 |     st.subheader("Short-term Actions (Next 30 Days)")
197 |     st.write("""
198 |     1. **Data Collection**
199 |        - Ensure complete customer data capture
200 |        - Implement regular satisfaction surveys
201 |     
202 |     2. **Quick Wins**
203 |        - Reach out to high-value customers at risk
204 |        - Fix common customer complaints
205 |        
206 |     3. **Analysis Refinement**
207 |        - Segment customers more precisely
208 |        - Identify key moments in the customer journey
209 |     """)
210 | 
211 | with col2:
212 |     st.subheader("Long-term Initiatives (3-6 Months)")
213 |     st.write("""
214 |     1. **Process Improvements**
215 |        - Optimize onboarding process
216 |        - Improve support response times
217 |        
218 |     2. **Value Enhancement**
219 |        - Refine product/service offering
220 |        - Review and adjust pricing strategy
221 |        
222 |     3. **Loyalty Program**
223 |        - Design tiered rewards system
224 |        - Implement early warning system for at-risk customers
225 |     """)
226 | 
227 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
228 | 
229 | # ROI Calculator
230 | st.header("Retention ROI Calculator")
231 | st.write("Estimate the return on investment for your customer retention initiatives")
232 | 
233 | col1, col2, col3 = st.columns(3)
234 | 
235 | with col1:
236 |     st.subheader("Inputs")
237 |     total_customers = st.number_input("Total customers", min_value=1, value=len(df))
238 |     avg_customer_value = st.number_input("Average annual customer value ($)", min_value=0, value=500)
239 |     current_churn = st.slider("Current churn rate (%)", min_value=0.0, max_value=100.0, value=float(churn_rate))
240 |     target_churn = st.slider("Target churn rate (%)", min_value=0.0, max_value=100.0, value=max(5.0, float(churn_rate)-5.0))
241 |     retention_cost = st.number_input("Cost per customer for retention program ($)", min_value=0, value=50)
242 | 
243 | with col2:
244 |     st.subheader("Calculation")
245 |     current_churned = int(total_customers * (current_churn / 100))
246 |     target_churned = int(total_customers * (target_churn / 100))
247 |     customers_saved = current_churned - target_churned
248 |     revenue_saved = customers_saved * avg_customer_value
249 |     program_cost = total_customers * retention_cost
250 |     net_benefit = revenue_saved - program_cost
251 |     roi = (net_benefit / program_cost * 100) if program_cost > 0 else 0
252 |     
253 |     st.metric("Customers retained", f"{customers_saved}")
254 |     st.metric("Revenue protected", f"${revenue_saved:,.2f}")
255 |     st.metric("Program cost", f"${program_cost:,.2f}")
256 | 
257 | with col3:
258 |     st.subheader("Results")
259 |     st.metric("Net benefit", f"${net_benefit:,.2f}")
260 |     st.metric("ROI", f"{roi:.1f}%")
261 |     
262 |     if roi > 100:
263 |         st.success("This program has excellent ROI potential!")
264 |     elif roi > 0:
265 |         st.info("This program has positive ROI potential.")
266 |     else:
267 |         st.error("This program may not be cost-effective. Consider adjusting.")
268 | 
269 | # Export section
270 | st.header("Export Insights")
271 | 
272 | # Using CSV as the only export format
273 | export_format = "CSV"
274 | st.info("Export will be in CSV format. Select data types to include below.")
275 | export_what = st.multiselect("Data to export:", ["Customer Segments", "Churn Risk Scores", "Recommendations"], 
276 |                             help="Select one or more data types to include in your report.")
277 | 
278 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
279 | 
280 | 
281 | if st.button("Generate Report"):
282 |     # Create a report DataFrame with requested information
283 |     if len(export_what) > 0:
284 |         # Start with the basic customer ID and churn columns
285 |         report_df = df[[ID_COL, TARGET_COL]].copy()
286 |         
287 |         # Add requested columns based on user selections
288 |         if 'segment' in df.columns and "Customer Segments" in export_what:
289 |             report_df['segment'] = df['segment']
290 |         
291 |         if "Churn Risk Scores" in export_what:
292 |             # For churn risk scores, create a simple score based on available data
293 |             if 'loyalty_score' in df.columns and 'days_since_last_purchase' in df.columns:
294 |                 # Create a risk score between 1-10 using loyalty and recency
295 |                 norm_loyalty = (df['loyalty_score'] - df['loyalty_score'].min()) / (df['loyalty_score'].max() - df['loyalty_score'].min())
296 |                 norm_recency = 1 - (df['days_since_last_purchase'] - df['days_since_last_purchase'].min()) / (df['days_since_last_purchase'].max() - df['days_since_last_purchase'].min())
297 |                 report_df['risk_score'] = 10 - ((norm_loyalty + norm_recency) / 2 * 10).round(1)
298 |             else:
299 |                 # Fallback: use churn value as risk indicator
300 |                 report_df['risk_score'] = df[TARGET_COL] * 10
301 |         
302 |         # If recommendations are selected, add them as text columns
303 |         if "Recommendations" in export_what:
304 |             # Add generic recommendations based on churn values
305 |             report_df['recommendation'] = np.where(
306 |                 df[TARGET_COL] == 1,
307 |                 "Reach out for win-back with personalized offer",
308 |                 "Send loyalty reward and upsell opportunity"
309 |             )
310 |             
311 |             # Determine priority based on available columns
312 |             if 'risk_score' in report_df.columns:
313 |                 # If risk score exists, use it for priority
314 |                 report_df['priority'] = np.where(
315 |                     report_df['risk_score'] > 5,
316 |                     "High",
317 |                     "Normal"
318 |                 )
319 |             else:
320 |                 # If no risk score, base priority on churn directly
321 |                 report_df['priority'] = np.where(
322 |                     df[TARGET_COL] == 1,
323 |                     "High",
324 |                     "Normal"
325 |                 )
326 |         
327 |         # Create a buffer to download the data
328 |         buffer = io.BytesIO()
329 |         
330 |         # Export as CSV
331 |         report_df.to_csv(buffer, index=False)
332 |         mime_type = "text/csv"
333 |         file_ext = "csv"
334 |         
335 |         # Offer the file for download
336 |         buffer.seek(0)
337 |         st.download_button(
338 |             label="Download Report",
339 |             data=buffer,
340 |             file_name=f"churn_analysis_report.{file_ext}",
341 |             mime=mime_type
342 |         )
343 |     else:
344 |         st.error("Please select at least one data category to export")
</content>
</file>
<file><path>app.py</path>
<content lines="1-304">
  1 | """
  2 | Customer Business Analysis Dashboard for E-commerce
  3 | 
  4 | This is our main app file that ties everything together. It's like the home page
  5 | where users start their journey through the dashboard. From here, they can load data,
  6 | see key metrics, and navigate to different pages.
  7 | 
  8 | No fancy stuff here just the essential tools businesses need to understand their customers better.
  9 | Think of it as a Swiss Army knife for customer data!
 10 | """
 11 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 12 | 
 13 | import streamlit as st
 14 | import pandas as pd
 15 | import numpy as np
 16 | import os
 17 | import sys
 18 | from pathlib import Path
 19 | 
 20 | # Add parent directory to path
 21 | sys.path.append(os.path.dirname(os.path.abspath(__file__)))
 22 | 
 23 | # Import utilities
 24 | from src.helpers import (
 25 |     SAMPLE_DATA_PATH, DB_PATH, 
 26 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, TARGET_COL, ID_COL,
 27 |     ensure_dir
 28 | )
 29 | from src.data_prep import load_csv, prepare_data_for_analysis
 30 | from src.sql_utils import create_db_and_table, upsert_clean_data
 31 | 
 32 | # Set page config
 33 | st.set_page_config(
 34 |     page_title="Business Analysis Dashboard",
 35 |     page_icon="�",
 36 |     layout="wide",
 37 |     initial_sidebar_state="expanded"
 38 | )
 39 | 
 40 | # Initialize session state
 41 | if 'data' not in st.session_state:
 42 |     st.session_state.data = None
 43 | if 'data_processed' not in st.session_state:
 44 |     st.session_state.data_processed = False
 45 | if 'db_created' not in st.session_state:
 46 |     st.session_state.db_created = os.path.exists(DB_PATH)
 47 | 
 48 | # App title and description
 49 | st.title("Supercharge Your Customer Strategy!")
 50 | 
 51 | st.markdown("""
 52 | ## Unlock the Hidden Potential in Your Customer Data!
 53 | 
 54 | This powerful dashboard transforms raw customer information into **game-changing business insights**. 
 55 | Discover what makes your customers tick, why they stay (or leave), and how to boost your bottom line!
 56 | 
 57 | ### What You'll Discover:
 58 | - **Reveal surprising patterns** in your customer data with eye-popping visualizations
 59 | - **Unearth valuable insights** with custom SQL queries anyone can use
 60 | - **Identify your VIP customers** and target them with laser precision
 61 | - **Spot at-risk customers** before they leave and win them back
 62 | - **Get brilliant, actionable ideas** to skyrocket your retention rates
 63 | 
 64 | **Get started now!** Load your data or try our sample dataset below.
 65 | """)
 66 | 
 67 | # Sidebar with data options
 68 | with st.sidebar:
 69 |     st.header("Fire Up Your Analysis!")
 70 |     
 71 |     # Load sample data button
 72 |     if st.button("Load Amazing Sample Data!"):
 73 |         # Check if sample data exists
 74 |         if os.path.exists(SAMPLE_DATA_PATH):
 75 |             with st.spinner("Loading sample data..."):
 76 |                 df = load_csv(SAMPLE_DATA_PATH)
 77 |                 if df is not None and not df.empty:
 78 |                     st.session_state.data = df
 79 |                     st.success(f"Loaded {len(df)} sample records! Now you can explore")
 80 |                 else:
 81 |                     st.error("Failed to load sample data")
 82 |         else:
 83 |             # Try to generate sample data
 84 |             st.info("Sample data not found. Generating synthetic data...")
 85 |             try:
 86 |                 # Run the data generation script
 87 |                 import subprocess
 88 |                 result = subprocess.run(["python", "data/generate_synthetic_data.py"], 
 89 |                                         capture_output=True, text=True)
 90 |                 
 91 |                 if os.path.exists(SAMPLE_DATA_PATH):
 92 |                     df = load_csv(SAMPLE_DATA_PATH)
 93 |                     if df is not None and not df.empty:
 94 |                         st.session_state.data = df
 95 |                         st.success(f"Generated and loaded {len(df)} sample records!")
 96 |                     else:
 97 |                         st.error("Failed to load generated data")
 98 |                 else:
 99 |                     st.error("Failed to generate sample data")
100 |                     st.code(result.stderr)
101 |             except Exception as e:
102 |                 st.error(f"Error generating sample data: {str(e)}")
103 |     
104 |     # Upload own data
105 |     st.subheader("Or Upload Your Own Fantastic Data!")
106 |     uploaded_file = st.file_uploader("Drop your CSV file here and let's make magic!", type=["csv"])
107 |     if uploaded_file is not None:
108 |         try:
109 |             df = pd.read_csv(uploaded_file)
110 |             
111 |             # Basic validation
112 |             required_cols = [ID_COL, TARGET_COL]
113 |             missing_cols = [col for col in required_cols if col not in df.columns]
114 |             
115 |             if missing_cols:
116 |                 st.error(f"Missing required columns: {', '.join(missing_cols)}")
117 |                 st.info(f"Required columns: {', '.join(required_cols)}")
118 |             else:
119 |                 st.session_state.data = df
120 |                 st.success(f"Uploaded {len(df)} records. Ready for analysis!")
121 |         except Exception as e:
122 |             st.error(f"Error uploading file: {str(e)}")
123 |     
124 |     # Save to database button
125 |     if st.session_state.data is not None:
126 |         if st.button("Blast Off to Database!"):
127 |             with st.spinner("Saving to database..."):
128 |                 # First apply data preparation steps
129 |                 processed_data = prepare_data_for_analysis(st.session_state.data)
130 |                 result = upsert_clean_data(processed_data)
131 |                 if result:
132 |                     st.session_state.db_created = True
133 |                     st.session_state.data_processed = True
134 |                     st.success("Data saved to database! SQL queries ready to go")
135 |                 else:
136 |                     st.error("Failed to save to database")
137 |     
138 |     # Help text
139 |     st.markdown("---")
140 |     st.subheader("Quick Start Guide")
141 |     st.markdown("""
142 |     1. Load our awesome sample data or upload your own
143 |     2. Dive into dazzling visualizations
144 |     3. Run powerful SQL queries (no tech skills needed!)
145 |     4. Group customers and discover hidden patterns
146 |     5. Get brilliant ideas to boost your business
147 |     """)
148 |     
149 |     # App info
150 |     st.markdown("---")
151 |     st.caption("Customer Insight Revolution | v2.0.0")
152 | 
153 | # Main page content
154 | if st.session_state.data is not None:
155 |     # Show a data preview
156 |     st.header("Your Amazing Data Preview")
157 |     st.write("Behold! A sneak peek at your customer goldmine:")
158 |     st.dataframe(st.session_state.data.head(5), use_container_width=True)
159 |     
160 |     # Data stats
161 |     st.subheader("Power Metrics at a Glance!")
162 |     col1, col2, col3, col4 = st.columns(4)
163 |     with col1:
164 |         st.metric("Total Customers", f"{len(st.session_state.data):,}")
165 |     with col2:
166 |         churn_rate = st.session_state.data[TARGET_COL].mean() * 100
167 |         st.metric("Churn Rate", f"{churn_rate:.1f}%")
168 |     with col3:
169 |         if 'avg_order_value' in st.session_state.data.columns:
170 |             avg_order = st.session_state.data['avg_order_value'].mean()
171 |             st.metric("Avg Order Value", f"${avg_order:.2f}")
172 |     with col4:
173 |         if 'tenure_months' in st.session_state.data.columns:
174 |             avg_tenure = st.session_state.data['tenure_months'].mean()
175 |             st.metric("Avg Customer Lifespan", f"{avg_tenure:.1f} months")
176 |     
177 |     st.markdown("---")
178 |     
179 |     # Business KPIs
180 |     st.header("Treasure Trove of Business Insights")
181 |     
182 |     # Calculate important metrics
183 |     active_customers = len(st.session_state.data[st.session_state.data[TARGET_COL] == 0])
184 |     churn_count = len(st.session_state.data[st.session_state.data[TARGET_COL] == 1])
185 |     
186 |     # Customer Lifetime Value calculation (if relevant columns exist)
187 |     if 'avg_order_value' in st.session_state.data.columns and 'tenure_months' in st.session_state.data.columns:
188 |         # Simplified CLV calculation
189 |         avg_monthly_revenue = st.session_state.data['avg_order_value'].mean()
190 |         avg_lifetime = st.session_state.data['tenure_months'].mean()
191 |         estimated_margin = 0.3  # Assuming 30% profit margin
192 |         clv = avg_monthly_revenue * avg_lifetime * estimated_margin
193 |     else:
194 |         clv = None
195 |     
196 |     # Display metrics in cards
197 |     metric_col1, metric_col2, metric_col3 = st.columns(3)
198 |     
199 |     with metric_col1:
200 |         st.markdown("### Active Customers")
201 |         st.markdown(f"<h2 style='text-align: center; color: #4ECDC4;'>{active_customers:,}</h2>", unsafe_allow_html=True)
202 |         retention_rate = active_customers / len(st.session_state.data) * 100
203 |         st.markdown(f"<p style='text-align: center;'>Retention Rate: {retention_rate:.1f}%</p>", unsafe_allow_html=True)
204 |     
205 |     with metric_col2:
206 |         st.markdown("### Churned Customers")
207 |         st.markdown(f"<h2 style='text-align: center; color: #FF6B6B;'>{churn_count:,}</h2>", unsafe_allow_html=True)
208 |         st.markdown(f"<p style='text-align: center;'>Churn Rate: {churn_rate:.1f}%</p>", unsafe_allow_html=True)
209 |     
210 |     with metric_col3:
211 |         st.markdown("### Customer Lifetime Value")
212 |         if clv:
213 |             st.markdown(f"<h2 style='text-align: center; color: #FFD166;'>${clv:.2f}</h2>", unsafe_allow_html=True)
214 |             st.markdown("<p style='text-align: center;'>Average value per customer</p>", unsafe_allow_html=True)
215 |         else:
216 |             st.markdown("<h2 style='text-align: center; color: #FFD166;'>N/A</h2>", unsafe_allow_html=True)
217 |             st.markdown("<p style='text-align: center;'>Insufficient data to calculate</p>", unsafe_allow_html=True)
218 | 
219 |     st.markdown("---")
220 | 
221 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
222 | 
223 |     # Navigation help
224 |     st.header("Your Adventure Map")
225 |     st.write("Embark on your data journey through these exciting destinations:")
226 |     
227 |     # Page descriptions with icons
228 |     col1, col2 = st.columns(2)
229 |     with col1:
230 |         st.markdown("### Data Exploration")
231 |         st.write("""
232 |         - **Uncover hidden gems** in your customer data
233 |         - **Spot exciting trends** that others miss
234 |         - **Create powerful SQL queries** with ease
235 |         - **Build eye-popping visualizations** instantly
236 |         """)
237 |         
238 |         st.markdown("### Customer Groups")
239 |         st.write("""
240 |         - **Discover your customer tribes** based on real behavior
241 |         - **Decode buying patterns** that drive purchases
242 |         - **Identify your VIP customers** worth pampering
243 |         - **Unlock special insights** for each customer group
244 |         """)
245 |     
246 |     with col2:
247 |         st.markdown("### Customer Retention")
248 |         st.write("""
249 |         - **Discover why customers leave** (and how to make them stay!)
250 |         - **Pinpoint loyalty patterns** across customer groups
251 |         - **Track retention trends** with stunning visuals
252 |         - **Connect the dots** between behavior and loyalty
253 |         """)
254 |         
255 |         st.markdown("### Business Insights")
256 |         st.write("""
257 |         - **Transform data into money-making actions**
258 |         - **Craft laser-targeted strategies** for each group
259 |         - **Calculate the profit impact** of your retention efforts
260 |         - **Generate brilliant action plans** your team will love
261 |         """)
262 | 
263 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
264 | 
265 | else:
266 |     # No data loaded yet
267 |     st.info("Ready for liftoff! Load our amazing sample data or upload your own to begin your data adventure!")
268 |     
269 |     # Show example of what the data should look like
270 |     st.subheader("Example Data Format")
271 |     
272 |     # Create example data
273 |     example_data = {
274 |         'customer_id': ['CUST000123', 'CUST000456', 'CUST000789'],
275 |         'age': [32, 45, 28],
276 |         'gender': ['Female', 'Male', 'Female'],
277 |         'region': ['Urban', 'Suburban', 'Rural'],
278 |         'total_orders': [15, 4, 8],
279 |         'avg_order_value': [75.20, 120.50, 55.30],
280 |         'days_since_last_purchase': [12, 90, 30],
281 |         'loyalty_score': [0.75, 0.30, 0.60],
282 |         'complaints': [0, 2, 1],
283 |         'payment_type': ['Credit Card', 'PayPal', 'Credit Card'],
284 |         'tenure_months': [24, 8, 12],
285 |         'is_promo_user': [0, 1, 0],
286 |         'churn': [0, 1, 0]
287 |     }
288 |     
289 |     example_df = pd.DataFrame(example_data)
290 |     st.dataframe(example_df, use_container_width=True)
291 |     
292 |     st.markdown("""
293 |     **Required columns:**
294 |     - `customer_id`: Unique customer identifier
295 |     - `churn`: Target variable (0 = retained, 1 = churned)
296 |     
297 |     **Recommended columns:**
298 |     - Demographic data (age, gender, region)
299 |     - Purchase history (total_orders, avg_order_value)
300 |     - Engagement metrics (days_since_last_purchase, loyalty_score)
301 |     - Other relevant features (complaints, payment_type, etc.)
302 |     """)
303 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
304 | 
</content>
</file>
<file><path>src/biz_metrics.py</path>
<content lines="1-397">
  1 | """
  2 | Business metrics for customer churn prediction app.
  3 | """
  4 | import pandas as pd
  5 | import numpy as np
  6 | 
  7 | from .helpers import COST_RETAIN, AVG_FUTURE_ORDERS
  8 | 
  9 | def calculate_revenue_impact(df, churn_prob_col, avg_order_value_col):
 10 |     """
 11 |     Calculate the expected revenue impact of churn
 12 |     """
 13 |     if df is None or df.empty:
 14 |         return {
 15 |             'error': "No data provided for revenue impact calculation."
 16 |         }
 17 |     
 18 |     if churn_prob_col not in df.columns:
 19 |         return {
 20 |             'error': f"Churn probability column '{churn_prob_col}' not found in data."
 21 |         }
 22 |     
 23 |     if avg_order_value_col not in df.columns:
 24 |         return {
 25 |             'error': f"Average order value column '{avg_order_value_col}' not found in data."
 26 |         }
 27 |     
 28 |     try:
 29 |         # Total customers
 30 |         total_customers = len(df)
 31 |         
 32 |         # Expected number of churners
 33 |         expected_churners = df[churn_prob_col].sum()
 34 |         expected_churn_rate = expected_churners / total_customers * 100
 35 |         
 36 |         # Expected revenue loss
 37 |         avg_order_value = df[avg_order_value_col].mean()
 38 |         expected_revenue_loss = expected_churners * avg_order_value * AVG_FUTURE_ORDERS
 39 |         
 40 |         # Per customer metrics
 41 |         avg_expected_loss_per_customer = expected_revenue_loss / total_customers
 42 |         
 43 |         # Results
 44 |         results = {
 45 |             'total_customers': total_customers,
 46 |             'expected_churners': expected_churners,
 47 |             'expected_churn_rate': expected_churn_rate,
 48 |             'avg_order_value': avg_order_value,
 49 |             'expected_revenue_loss': expected_revenue_loss,
 50 |             'avg_expected_loss_per_customer': avg_expected_loss_per_customer
 51 |         }
 52 |         
 53 |         return results
 54 |     
 55 |     except Exception as e:
 56 |         print(f"Error calculating revenue impact: {e}")
 57 |         return {
 58 |             'error': f"Revenue impact calculation failed: {str(e)}"
 59 |         }
 60 | 
 61 | def calculate_targeting_roi(df, churn_prob_col, avg_order_value_col, risk_band_col=None):
 62 |     """
 63 |     Calculate ROI for targeting different risk segments
 64 |     """
 65 |     if df is None or df.empty:
 66 |         return {
 67 |             'error': "No data provided for ROI calculation."
 68 |         }
 69 |     
 70 |     if churn_prob_col not in df.columns:
 71 |         return {
 72 |             'error': f"Churn probability column '{churn_prob_col}' not found in data."
 73 |         }
 74 |     
 75 |     if avg_order_value_col not in df.columns:
 76 |         return {
 77 |             'error': f"Average order value column '{avg_order_value_col}' not found in data."
 78 |         }
 79 |     
 80 |     try:
 81 |         # Make a copy of the data
 82 |         df_calc = df.copy()
 83 |         
 84 |         # Sort by churn probability (descending)
 85 |         df_calc = df_calc.sort_values(churn_prob_col, ascending=False)
 86 |         
 87 |         # Calculate potential loss per customer
 88 |         df_calc['potential_loss'] = df_calc[avg_order_value_col] * AVG_FUTURE_ORDERS
 89 |         
 90 |         # Calculate expected loss (probability × potential loss)
 91 |         df_calc['expected_loss'] = df_calc[churn_prob_col] * df_calc['potential_loss']
 92 |         
 93 |         # Calculate retention cost
 94 |         df_calc['retention_cost'] = COST_RETAIN
 95 |         
 96 |         # Calculate expected benefit (expected loss - retention cost)
 97 |         df_calc['expected_benefit'] = df_calc['expected_loss'] - df_calc['retention_cost']
 98 |         
 99 |         # Calculate cumulative metrics at different targeting thresholds
100 |         results = []
101 |         
102 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
103 |         
104 |         # Calculate total expected loss
105 |         total_expected_loss = df_calc['expected_loss'].sum()
106 |         
107 |         # Get risk bands if available
108 |         has_risk_bands = risk_band_col in df_calc.columns
109 |         
110 |         if has_risk_bands:
111 |             # Calculate metrics for each risk band
112 |             for band in ['High Risk', 'Medium Risk', 'Low Risk']:
113 |                 band_df = df_calc[df_calc[risk_band_col] == band]
114 |                 
115 |                 if len(band_df) == 0:
116 |                     continue
117 |                 
118 |                 customers_count = len(band_df)
119 |                 total_retention_cost = customers_count * COST_RETAIN
120 |                 expected_loss_saved = band_df['expected_loss'].sum()
121 |                 expected_benefit = expected_loss_saved - total_retention_cost
122 |                 percentage_targeted = customers_count / len(df_calc) * 100
123 |                 
124 |                 results.append({
125 |                     'segment': band,
126 |                     'customers_count': customers_count,
127 |                     'percentage_targeted': percentage_targeted,
128 |                     'total_retention_cost': total_retention_cost,
129 |                     'expected_loss_saved': expected_loss_saved,
130 |                     'expected_benefit': expected_benefit,
131 |                     'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0
132 |                 })
133 |         
134 |         # Calculate metrics for different targeting percentages
135 |         percentiles = range(10, 101, 10)
136 |         
137 |         for p in percentiles:
138 |             cutoff_idx = int(len(df_calc) * p / 100)
139 |             targeted_df = df_calc.iloc[:cutoff_idx]
140 |             
141 |             customers_count = len(targeted_df)
142 |             total_retention_cost = customers_count * COST_RETAIN
143 |             expected_loss_saved = targeted_df['expected_loss'].sum()
144 |             expected_benefit = expected_loss_saved - total_retention_cost
145 |             
146 |             results.append({
147 |                 'segment': f"Top {p}%",
148 |                 'customers_count': customers_count,
149 |                 'percentage_targeted': p,
150 |                 'total_retention_cost': total_retention_cost,
151 |                 'expected_loss_saved': expected_loss_saved,
152 |                 'expected_benefit': expected_benefit,
153 |                 'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0,
154 |                 'percent_of_total_loss': expected_loss_saved / total_expected_loss * 100 if total_expected_loss > 0 else 0
155 |             })
156 |         
157 |         return {
158 |             'by_segment': results,
159 |             'total_expected_loss': total_expected_loss
160 |         }
161 |     
162 |     except Exception as e:
163 |         print(f"Error calculating targeting ROI: {e}")
164 |         return {
165 |             'error': f"ROI calculation failed: {str(e)}"
166 |         }
167 |     
168 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
169 | 
170 | 
171 | def get_retention_playbook_by_risk(risk_band):
172 |     """
173 |     Get retention playbook recommendations based on risk band
174 |     """
175 |     if risk_band == "High Risk":
176 |         actions = [
177 |             "Send personalized email with 20% discount coupon valid for 7 days",
178 |             "Follow up with a phone call from customer service within 48 hours",
179 |             "Offer free expedited shipping on next order",
180 |             "Add loyalty points boost (2x points for next 30 days)",
181 |             "Invite to exclusive product preview or early access"
182 |         ]
183 |     elif risk_band == "Medium Risk":
184 |         actions = [
185 |             "Send email with 10% discount coupon valid for 14 days",
186 |             "Recommend products based on previous purchases",
187 |             "Send reminder about loyalty points balance and upcoming expiration",
188 |             "Share new product announcements in their favorite categories",
189 |             "Ask for feedback or product review with small incentive"
190 |         ]
191 |     else:  # Low Risk
192 |         actions = [
193 |             "Include in regular marketing newsletters",
194 |             "Maintain standard loyalty program communications",
195 |             "Periodic engagement with seasonal promotions",
196 |             "Anniversary or birthday special offers",
197 |             "Invite to refer friends with dual incentives"
198 |         ]
199 |     
200 |     return actions
201 | 
202 | def get_targeting_recommendations(roi_results):
203 |     """
204 |     Get recommendations based on ROI calculations
205 |     """
206 |     if 'error' in roi_results:
207 |         return [
208 |             "Couldn't calculate targeting recommendations due to an error.",
209 |             "Please ensure your data includes churn probabilities and order values."
210 |         ]
211 |     
212 |     recommendations = []
213 |     
214 |     # Get segment data
215 |     segments = roi_results.get('by_segment', [])
216 |     total_expected_loss = roi_results.get('total_expected_loss', 0)
217 |     
218 |     # Find best ROI segment
219 |     best_roi_segment = None
220 |     best_roi = 0
221 |     
222 |     for segment in segments:
223 |         if segment['roi_ratio'] > best_roi:
224 |             best_roi = segment['roi_ratio']
225 |             best_roi_segment = segment
226 |     
227 |     if best_roi_segment:
228 |         if 'High Risk' in best_roi_segment.get('segment', ''):
229 |             recommendations.append(
230 |                 f"Focus on High Risk customers first - each $1 spent on retention saves ${best_roi:.2f} in revenue!"
231 |             )
232 |         elif 'Top' in best_roi_segment.get('segment', ''):
233 |             recommendations.append(
234 |                 f"Target the {best_roi_segment['segment']} of customers for best ROI - each $1 spent saves ${best_roi:.2f}!"
235 |             )
236 |     
237 |     # Find optimal targeting percentage
238 |     optimal_segment = None
239 |     max_benefit = 0
240 |     
241 |     for segment in segments:
242 |         if 'Top' in segment.get('segment', '') and segment['expected_benefit'] > max_benefit:
243 |             max_benefit = segment['expected_benefit']
244 |             optimal_segment = segment
245 |     
246 |     if optimal_segment:
247 |         recommendations.append(
248 |             f"Optimal targeting strategy: {optimal_segment['segment']} of customers (saves ${optimal_segment['expected_benefit']:.2f})"
249 |         )
250 |     
251 |     # Add general recommendations
252 |     recommendations.extend([
253 |         f"Total expected loss from churn: ${total_expected_loss:.2f} - this is what we're trying to prevent!",
254 |         "Customize retention offers based on customer value and risk level for best results",
255 |         "Track campaign performance and adjust targeting thresholds over time"
256 |     ])
257 |     
258 |     return recommendations
259 | 
260 | def generate_business_report(df, churn_predictions, feature_importance, cost_benefit_df=None):
261 |     """
262 |     Generate a business report with insights and recommendations
263 |     """
264 |     if df is None or df.empty:
265 |         return "No data available for business report."
266 |     
267 |     # Calculate basic metrics
268 |     total_customers = len(df)
269 |     churn_rate = df['churn'].mean() * 100 if 'churn' in df.columns else None
270 |     
271 |     # Start building the report
272 |     report = "# Customer Churn Business Report\n\n"
273 |     
274 |     # Current situation
275 |     report += "## Current Situation\n\n"
276 |     
277 |     if churn_rate is not None:
278 |         report += f"- Current churn rate: **{churn_rate:.1f}%** of customers\n"
279 |     
280 |     # Get average order value and tenure
281 |     avg_order = df['avg_order_value'].mean() if 'avg_order_value' in df.columns else None
282 |     avg_tenure = df['tenure_months'].mean() if 'tenure_months' in df.columns else None
283 |     
284 |     if avg_order is not None:
285 |         report += f"- Average order value: **${avg_order:.2f}**\n"
286 |     
287 |     if avg_tenure is not None:
288 |         report += f"- Average customer tenure: **{avg_tenure:.1f} months**\n"
289 |     
290 |     # Risky segments
291 |     report += "\n## High-Risk Customer Segments\n\n"
292 |     
293 |     # By region if available
294 |     if 'region' in df.columns:
295 |         churn_by_region = df.groupby('region')['churn'].mean().sort_values(ascending=False)
296 |         highest_region = churn_by_region.index[0]
297 |         highest_region_rate = churn_by_region.iloc[0] * 100
298 |         
299 |         report += f"- **{highest_region} region** has highest churn rate at {highest_region_rate:.1f}%\n"
300 |     
301 |     # By payment type if available
302 |     if 'payment_type' in df.columns:
303 |         churn_by_payment = df.groupby('payment_type')['churn'].mean().sort_values(ascending=False)
304 |         highest_payment = churn_by_payment.index[0]
305 |         highest_payment_rate = churn_by_payment.iloc[0] * 100
306 |         
307 |         report += f"- **{highest_payment} payment** users churn at {highest_payment_rate:.1f}%\n"
308 |     
309 |     # By tenure buckets if available
310 |     if 'tenure_months' in df.columns:
311 |         df['tenure_bucket'] = pd.cut(
312 |             df['tenure_months'], 
313 |             bins=[0, 6, 12, 24, 36, float('inf')],
314 |             labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
315 |         )
316 |         churn_by_tenure = df.groupby('tenure_bucket')['churn'].mean().sort_values(ascending=False)
317 |         highest_tenure = churn_by_tenure.index[0]
318 |         highest_tenure_rate = churn_by_tenure.iloc[0] * 100
319 |         
320 |         report += f"- Customers in **{highest_tenure}** tenure bracket churn at {highest_tenure_rate:.1f}%\n"
321 |     
322 |     # Key drivers section
323 |     report += "\n## Top 5 Churn Drivers\n\n"
324 |     
325 |     # Use feature importance if available
326 |     if feature_importance and len(feature_importance) > 0:
327 |         for i, feature in enumerate(feature_importance[:5], 1):
328 |             name = feature.get('feature', '')
329 |             explanation = feature.get('explanation', '')
330 |             
331 |             report += f"{i}. **{name}**: {explanation}\n"
332 |     else:
333 |         report += "Feature importance data not available.\n"
334 | 
335 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
336 | 
337 |     # Targeting plan
338 |     report += "\n## Targeting Plan\n\n"
339 |     
340 |     if cost_benefit_df is not None and not cost_benefit_df.empty:
341 |         # Find optimal targeting percentage
342 |         optimal_row = cost_benefit_df.loc[cost_benefit_df['net_benefit'].idxmax()]
343 |         optimal_percent = optimal_row['targeting_percent']
344 |         optimal_benefit = optimal_row['net_benefit']
345 |         optimal_customers = optimal_row['customers_targeted']
346 |         optimal_churners = optimal_row['churners_caught']
347 |         optimal_churners_pct = optimal_row['churners_caught_percent']
348 |         
349 |         report += f"- **Optimal strategy**: Target top {optimal_percent:.0f}% highest-risk customers\n"
350 |         report += f"- This means focusing on **{optimal_customers:.0f} customers**\n"
351 |         report += f"- Expected to save **${optimal_benefit:.2f}** in revenue\n"
352 |         report += f"- Would catch **{optimal_churners:.0f} churners** ({optimal_churners_pct:.1f}% of all churners)\n"
353 |     else:
354 |         report += "Cost-benefit analysis data not available.\n"
355 |     
356 |     # Action items
357 |     report += "\n## Recommended Actions\n\n"
358 |     
359 |     # High risk actions
360 |     report += "### For High-Risk Customers:\n"
361 |     report += "1. Send personalized email with 20% discount coupon valid for 7 days\n"
362 |     report += "2. Follow up with a phone call from customer service within 48 hours\n"
363 |     report += "3. Offer free expedited shipping on next order\n"
364 |     
365 |     # Medium risk actions
366 |     report += "\n### For Medium-Risk Customers:\n"
367 |     report += "1. Send email with 10% discount coupon valid for 14 days\n"
368 |     report += "2. Recommend products based on previous purchases\n"
369 |     report += "3. Send reminder about loyalty points balance\n"
370 |     
371 |     # Product/service improvements
372 |     report += "\n### Product/Service Improvements:\n"
373 |     
374 |     # Look at complaints if available
375 |     if 'complaints' in df.columns and df['complaints'].sum() > 0:
376 |         report += "1. Address common customer complaints to improve retention\n"
377 |     else:
378 |         report += "1. Review customer feedback for product improvement opportunities\n"
379 |     
380 |     report += "2. Consider loyalty program adjustments for better engagement\n"
381 |     report += "3. Improve onboarding for new customers (first 6 months critical)\n"
382 |     
383 |     # 30-day roadmap
384 |     report += "\n## Next 30 Days Roadmap\n\n"
385 |     report += "1. **Week 1**: Launch high-risk customer retention campaign\n"
386 |     report += "2. **Week 2**: Begin medium-risk customer engagement\n"
387 |     report += "3. **Week 3**: Analyze initial campaign results and adjust\n"
388 |     report += "4. **Week 4**: Prepare follow-up actions and long-term strategy\n"
389 |     
390 |     # Final notes
391 |     report += "\n## Notes\n\n"
392 |     report += "- This is an initial analysis based on available data\n"
393 |     report += "- Campaign effectiveness should be measured and tactics adjusted\n"
394 |     report += "- Consider A/B testing different retention offers\n"
395 |     report += "- Long-term product/service improvements will have most sustainable impact\n"
396 |     
397 |     return report
</content>
</file>
<file><path>README.md</path>
<content lines="1-167">
  1 | # ⚠️ PROTECTED CODE - DO NOT COPY ⚠️
  2 | 
  3 | This is a Team project by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). This repository is publicly visible for demonstration purposes only.
  4 | 
  5 | Author: Meet Jain & Aditi Gopinath
  6 | - This project is protected. Do not copy, fork, or reuse without permission.
  7 | - Unauthorized use is strictly prohibited. Only the official deployment is allowed to run.
  8 | 
  9 | ## Legal Protection
 10 | This project is protected by copyright law and includes proprietary security measures. Unauthorized use or attempts to circumvent security measures may result in legal consequences.
 11 | 
 12 | ## Contact
 13 | For any inquiries about this project please contact: meetofficialhere@gmail.com
 14 | 
 15 | # Customer Business Analysis Dashboard
 16 | 
 17 | A powerful, easy-to-use dashboard for analyzing customer behavior, identifying segments, and preventing customer churn.
 18 | 
 19 | ## Overview
 20 | 
 21 | This dashboard helps businesses understand their customers better and make smart decisions to keep them happy. It takes customer data, shows important patterns, and gives actionable advice that anyone can understand - no fancy statistics degree needed!
 22 | 
 23 | ## Features
 24 | 
 25 | The dashboard comes packed with tools that make customer analysis simple:
 26 | 
 27 | - **See Your Data Come to Life**: Interactive charts that show customer patterns anyone can understand
 28 | - **Ask Questions Using SQL**: Run simple queries to dig into your customer data
 29 | - **Group Similar Customers**: Automatically sort customers into meaningful groups
 30 | - **Spot Why Customers Leave**: Find the real reasons behind customer churn
 31 | - **Get Plain-English Advice**: Receive clear recommendations anyone can implement
 32 | 
 33 | ## Dashboard Pages
 34 | 
 35 | Our dashboard has four main sections:
 36 | 
 37 | 1. **Data Explorer**: Look at your customer data in different ways and spot patterns
 38 | 2. **Customer Groups**: See which types of customers you have and how they behave
 39 | 3. **Churn Analysis**: Understand why customers leave and who's at risk
 40 | 4. **Recommendations**: Get practical advice on keeping customers happy
 41 | 
 42 | ## Architecture
 43 | 
 44 | The dashboard is built with a clean, modular structure that makes it easy to understand and extend.
 45 | 
 46 | ```
 47 | ┌─────────────────────────────────────┐
 48 | │           Web Interface             │
 49 | │    (Streamlit Interactive Pages)    │
 50 | └───────────────┬─────────────────────┘
 51 |                 │
 52 | ┌───────────────▼─────────────────────┐
 53 | │         Business Logic Layer         │
 54 | │   (Data Analysis & Visualization)   │
 55 | └───────────────┬─────────────────────┘
 56 |                 │
 57 | ┌───────────────▼─────────────────────┐
 58 | │           Data Access Layer          │
 59 | │      (CSV Import & SQLite DB)       │
 60 | └─────────────────────────────────────┘
 61 | ```
 62 | 
 63 | ### Component Diagram
 64 | 
 65 | ```
 66 | ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
 67 | │  Data Input  │───▶│  Processing   │───▶│ Visualization│
 68 | │  & Storage   │    │  & Analysis   │    │  & Reports   │
 69 | └──────────────┘    └───────────────┘    └──────────────┘
 70 |        │                   │                    │
 71 |        ▼                   ▼                    ▼
 72 | ┌──────────────┐    ┌───────────────┐    ┌──────────────┐
 73 | │ CSV Importer │    │ Segmentation  │    │ Interactive  │
 74 | │ SQLite DB    │    │ Churn Models  │    │ Dashboards   │
 75 | └──────────────┘    └───────────────┘    └──────────────┘
 76 | ```
 77 | 
 78 | ## How to Use the Dashboard
 79 | 
 80 | ### Getting Started
 81 | 
 82 | When you open the dashboard, you'll see a home page with these options:
 83 | 
 84 | 1. **Load Sample Data**: Click this button to try out the dashboard with example data
 85 | 2. **Upload Your Own Data**: Upload your customer data file (CSV format)
 86 | 3. **Save to Database**: Store your data for faster access next time
 87 | 
 88 | ### Understanding Your Customers
 89 | 
 90 | Once your data is loaded, you can:
 91 | 
 92 | - **See Key Numbers**: Total customers, churn rate, and customer value at a glance
 93 | - **Explore Different Pages**: Use the sidebar to navigate between dashboard sections
 94 | - **Download Reports**: Export insights as CSV files to share with your team
 95 | 
 96 | ### Data You Can Use
 97 | 
 98 | To get the most from this dashboard, your customer data should include:
 99 | 
100 | - **Must Have**:
101 |   - `customer_id`: A unique number/code for each customer
102 |   - `churn`: Whether they've left (1) or stayed (0)
103 | 
104 | - **Good to Have**:
105 |   - **Who they are**: Age, gender, location
106 |   - **What they buy**: Number of orders, average spending
107 |   - **How they engage**: Days since last purchase, loyalty points
108 |   - **Customer experience**: Number of complaints
109 |   - **Other useful info**: Payment method, months as customer, etc.
110 | 
111 | Sample data is included if you just want to try things out!
112 | 
113 | ## Project Organization
114 | 
115 | The project is organized into these key folders:
116 | 
117 | ```
118 | Customer-Churn-Dashboard/
119 | ├── app.py                # Main dashboard entry point
120 | ├── requirements.txt      # Python package dependencies
121 | ├── .streamlit/           # Streamlit configuration
122 | ├── data/                 # Data files and database
123 | │   └── sample_churn.csv  # Example customer dataset
124 | ├── pages/                # Dashboard page files
125 | │   ├── 1_EDA_and_SQL_Checks.py           # Data exploration page
126 | │   ├── 2_Customer_Segments.py            # Customer segmentation page
127 | │   ├── 3_Churn_Analysis.py               # Churn analysis page
128 | │   └── 4_Insights_and_Recommendations.py  # Insights page
129 | └── src/                  # Source code modules
130 |     ├── data_prep.py      # Data preparation functions
131 |     ├── helpers.py        # Helper utilities and constants
132 |     └── sql_utils.py      # Database functions
133 | ```
134 | 
135 | ## Analysis Methods Made Simple
136 | 
137 | The dashboard uses these business techniques, explained in plain language:
138 | 
139 | 1. **RFM Grouping**: Groups customers based on:
140 |    - How Recently they purchased
141 |    - How Frequently they buy
142 |    - How Much Money they spend
143 | 
144 | 2. **Customer Journey**: Tracks how customers behave over time from when they first joined
145 | 
146 | 3. **Churn Reasons**: Finds the real factors that make customers leave
147 | 
148 | 4. **Customer Value**: Shows how much a customer is worth to your business long-term
149 | 
150 | 5. **Ask Your Own Questions**: Use simple SQL queries to answer specific business questions
151 | 
152 | ## License
153 | 
154 | This project is licensed under the MIT License - see the LICENSE file for details.
155 | 
156 | ## Contact
157 | 
158 | Connect us through the following platforms:
159 | 
160 | ### Professional Networking
161 | [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/meet-jain-413015265/)
162 | [![Twitter](https://img.shields.io/badge/Twitter-1DA1F2?style=flat&logo=twitter&logoColor=white)](https://twitter.com/Meetjain_100)
163 | 
164 | ### Social Media and Platforms
165 | [![Discord](https://img.shields.io/badge/Discord-7289DA?style=flat&logo=discord&logoColor=white)](https://discordapp.com/users/meetofficial)
166 | [![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=flat&logo=instagram&logoColor=white)](https://www.instagram.com/m.jain_17/)
167 | 
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
docs/SEGMENTATION_PLAN_SUMMARY.md

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:55:18.593Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze the current implementation and design comprehensive solutions for both the customer retention/churn prediction dashboard and the business insights page.

<read_file>
<args>
  <file>
    <path>src/helpers.py</path>
  </file>
  <file>
    <path>src/data_prep.py</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'src/helpers.py', 'src/data_prep.py'] Result:
<files>
<file><path>src/helpers.py</path>
<content lines="1-109">
  1 | """
  2 | The Helper's Toolbox - Making Life Easier!
  3 | 
  4 | This file has all those handy tools and settings that we use throughout the dashboard.
  5 | It's like the utility belt that keeps everything running smoothly.
  6 | 
  7 | No rocket science here - just practical functions that save us time and keep things consistent.
  8 | """
  9 | import os
 10 | import pandas as pd
 11 | import numpy as np
 12 | from pathlib import Path
 13 | 
 14 | # Root dir
 15 | ROOT_DIR = Path(__file__).parent.parent
 16 | 
 17 | # Data paths
 18 | DATA_DIR = os.path.join(ROOT_DIR, "data")
 19 | SAMPLE_DATA_PATH = os.path.join(DATA_DIR, "sample_churn.csv")
 20 | DB_PATH = os.path.join(DATA_DIR, "app.db")
 21 | 
 22 | # Data config
 23 | TARGET_COL = "churn"
 24 | 
 25 | # Feature groups
 26 | NUMERIC_COLS = [
 27 |     "age", 
 28 |     "total_orders", 
 29 |     "avg_order_value", 
 30 |     "days_since_last_purchase", 
 31 |     "loyalty_score", 
 32 |     "complaints", 
 33 |     "tenure_months"
 34 | ]
 35 | 
 36 | CATEGORICAL_COLS = [
 37 |     "gender", 
 38 |     "region", 
 39 |     "payment_type"
 40 | ]
 41 | 
 42 | BINARY_COLS = [
 43 |     "is_promo_user"
 44 | ]
 45 | 
 46 | ID_COL = "customer_id"
 47 | 
 48 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 49 | # All features (excluding target and id)
 50 | FEATURE_COLS = NUMERIC_COLS + CATEGORICAL_COLS + BINARY_COLS
 51 | 
 52 | # Business config
 53 | COST_RETAIN = 50  # cost of retention offer
 54 | AVG_FUTURE_ORDERS = 3  # expected future orders if customer stays
 55 | 
 56 | # Simple helper to check if a directory exists, if not create it
 57 | def ensure_dir(directory):
 58 |     """Make sure directory exists, if not create it"""
 59 |     if not os.path.exists(directory):
 60 |         os.makedirs(directory)
 61 |         print(f"Created directory: {directory}")
 62 |     return directory
 63 | 
 64 | def get_risk_band(churn_value):
 65 |     """Convert churn value to risk band based on business rules"""
 66 |     if churn_value == 1:
 67 |         return "High Risk"
 68 |     else:
 69 |         return "Low Risk"
 70 | 
 71 | def calculate_days_recency_score(days_since_purchase):
 72 |     """Calculate recency score based on days since last purchase"""
 73 |     if days_since_purchase <= 30:
 74 |         return 3  # Recently active
 75 |     elif days_since_purchase <= 90:
 76 |         return 2  # Active but slipping
 77 |     else:
 78 |         return 1  # Inactive
 79 | 
 80 | def calculate_frequency_score(total_orders):
 81 |     """Calculate frequency score based on total orders"""
 82 |     if total_orders >= 10:
 83 |         return 3  # Frequent buyer
 84 |     elif total_orders >= 5:
 85 |         return 2  # Regular buyer
 86 |     else:
 87 |         return 1  # Occasional buyer
 88 | 
 89 | def calculate_monetary_score(avg_order_value):
 90 |     """Calculate monetary score based on average order value"""
 91 |     if avg_order_value >= 100:
 92 |         return 3  # High value
 93 |     elif avg_order_value >= 50:
 94 |         return 2  # Medium value
 95 |     else:
 96 |         return 1  # Low value
 97 | 
 98 | def calculate_rfm_score(days_since_purchase, total_orders, avg_order_value):
 99 |     """Calculate RFM score for customer segmentation"""
100 |     r_score = calculate_days_recency_score(days_since_purchase)
101 |     f_score = calculate_frequency_score(total_orders)
102 |     m_score = calculate_monetary_score(avg_order_value)
103 |     
104 |     return {
105 |         'recency_score': r_score,
106 |         'frequency_score': f_score,
107 |         'monetary_score': m_score,
108 |         'total_score': r_score + f_score + m_score
109 |     }
</content>
</file>
<file><path>src/data_prep.py</path>
<content lines="1-219">
  1 | """
  2 | Data preparation functions for customer churn analysis dashboard.
  3 | """
  4 | import pandas as pd
  5 | import numpy as np
  6 | import os
  7 | from sklearn.impute import SimpleImputer
  8 | 
  9 | from .helpers import (
 10 |     NUMERIC_COLS, CATEGORICAL_COLS, BINARY_COLS, 
 11 |     TARGET_COL, ID_COL, FEATURE_COLS,
 12 |     ensure_dir, calculate_rfm_score, get_risk_band
 13 | )
 14 | 
 15 | def load_csv(path):
 16 |     """Load CSV file into pandas DataFrame"""
 17 |     try:
 18 |         print(f"Loading data from {path}...")
 19 |         df = pd.read_csv(path)
 20 |         print(f"Loaded {df.shape[0]} rows and {df.shape[1]} columns. not bad!")
 21 |         return df
 22 |     except Exception as e:
 23 |         print(f"Error loading data: {e}")
 24 |         return None
 25 | 
 26 | def basic_clean(df):
 27 |     """Basic cleaning - trim strings, fix weird values, cast dtypes, drop dupes"""
 28 |     if df is None or df.empty:
 29 |         print("No data to clean, sad :(")
 30 |         return None
 31 |     
 32 |     print("Starting basic cleaning...")
 33 |     
 34 |     # Make a copy to avoid modifying original
 35 |     df_clean = df.copy()
 36 |     
 37 |     # Check if we have the expected columns
 38 |     missing_cols = []
 39 |     expected_cols = FEATURE_COLS + [TARGET_COL, ID_COL]
 40 | 
 41 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 42 |     
 43 |     for col in expected_cols:
 44 |         if col not in df_clean.columns:
 45 |             missing_cols.append(col)
 46 |     
 47 |     if missing_cols:
 48 |         print(f"Warning: Missing expected columns: {missing_cols}")
 49 |         print("Will continue with columns we have, fingers crossed...")
 50 |     
 51 |     # Drop duplicates
 52 |     old_shape = df_clean.shape[0]
 53 |     df_clean = df_clean.drop_duplicates()
 54 |     if old_shape > df_clean.shape[0]:
 55 |         print(f"Dropped {old_shape - df_clean.shape[0]} duplicate rows, sneaky dupes!")
 56 |     
 57 |     # Trim string columns
 58 |     for col in df_clean.select_dtypes(include=['object']).columns:
 59 |         df_clean[col] = df_clean[col].str.strip() if hasattr(df_clean[col], 'str') else df_clean[col]
 60 |     
 61 |     # Fix data types
 62 |     if ID_COL in df_clean.columns:
 63 |         df_clean[ID_COL] = df_clean[ID_COL].astype(str)
 64 |     
 65 |     for col in NUMERIC_COLS:
 66 |         if col in df_clean.columns:
 67 |             try:
 68 |                 df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
 69 |             except:
 70 |                 print(f"Couldn't convert {col} to numeric, weird values maybe?")
 71 |     
 72 |     for col in BINARY_COLS:
 73 |         if col in df_clean.columns:
 74 |             df_clean[col] = df_clean[col].astype(int)
 75 |     
 76 |     if TARGET_COL in df_clean.columns:
 77 |         df_clean[TARGET_COL] = df_clean[TARGET_COL].astype(int)
 78 |     
 79 |     print(f"Basic cleaning complete! We have {df_clean.shape[0]} rows now. cool.")
 80 |     return df_clean
 81 | 
 82 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
 83 | 
 84 | def handle_missing(df):
 85 |     """Handle missing values with simple imputations"""
 86 |     if df is None or df.empty:
 87 |         print("No data to handle missing values, bummer")
 88 |         return None
 89 |     
 90 |     print("Looking for missing values...")
 91 |     
 92 |     # Check if we have missing values
 93 |     missing_counts = df.isnull().sum()
 94 |     missing_cols = missing_counts[missing_counts > 0]
 95 |     
 96 |     if len(missing_cols) == 0:
 97 |         print("No missing values found! lucky us.")
 98 |         return df
 99 |     
100 |     print(f"Found missing values in {len(missing_cols)} columns. gonna fix em...")
101 |     
102 |     # Make a copy to avoid modifying original
103 |     df_clean = df.copy()
104 |     
105 |     # Impute numeric columns with median
106 |     num_imputer = SimpleImputer(strategy='median')
107 |     num_cols_to_impute = [col for col in NUMERIC_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
108 |     
109 |     if num_cols_to_impute:
110 |         print(f"Filling {len(num_cols_to_impute)} numeric columns with median values")
111 |         df_clean[num_cols_to_impute] = num_imputer.fit_transform(df_clean[num_cols_to_impute])
112 |     
113 |     # Impute categorical columns with most frequent value
114 |     cat_imputer = SimpleImputer(strategy='most_frequent')
115 |     cat_cols_to_impute = [col for col in CATEGORICAL_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
116 |     
117 |     if cat_cols_to_impute:
118 |         print(f"Filling {len(cat_cols_to_impute)} categorical columns with most common values")
119 |         df_clean[cat_cols_to_impute] = cat_imputer.fit_transform(df_clean[cat_cols_to_impute])
120 |     
121 |     # Binary columns (fill with 0 which is safer)
122 |     bin_cols_to_impute = [col for col in BINARY_COLS if col in df_clean.columns and df_clean[col].isnull().sum() > 0]
123 |     
124 |     if bin_cols_to_impute:
125 |         print(f"Filling {len(bin_cols_to_impute)} binary columns with 0s")
126 |         for col in bin_cols_to_impute:
127 |             df_clean[col] = df_clean[col].fillna(0)
128 |     
129 |     # Check if we've resolved all missing values
130 |     remaining_missing = df_clean.isnull().sum().sum()
131 |     if remaining_missing > 0:
132 |         print(f"Warning: Still have {remaining_missing} missing values. thats weird :/")
133 |     else:
134 |         print("All missing values handled! nice and clean now.")
135 |     
136 |     return df_clean
137 | 
138 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
139 | 
140 | def add_derived_features(df):
141 |     """Add derived features for analysis"""
142 |     if df is None or df.empty:
143 |         print("No data to add derived features to")
144 |         return df
145 |     
146 |     df_derived = df.copy()
147 |     
148 |     # Calculate risk band
149 |     if TARGET_COL in df_derived.columns:
150 |         df_derived['risk_band'] = df_derived[TARGET_COL].apply(get_risk_band)
151 |     
152 |     # Create RFM segments if we have the necessary columns
153 |     required_cols = ['days_since_last_purchase', 'total_orders', 'avg_order_value']
154 |     if all(col in df_derived.columns for col in required_cols):
155 |         print("Adding RFM scores and segments...")
156 |         
157 |         # Apply RFM scoring function
158 |         rfm_scores = df_derived.apply(
159 |             lambda row: calculate_rfm_score(
160 |                 row['days_since_last_purchase'], 
161 |                 row['total_orders'], 
162 |                 row['avg_order_value']
163 |             ), 
164 |             axis=1
165 |         )
166 |         
167 |         # Extract individual scores
168 |         df_derived['recency_score'] = rfm_scores.apply(lambda x: x['recency_score'])
169 |         df_derived['frequency_score'] = rfm_scores.apply(lambda x: x['frequency_score'])
170 |         df_derived['monetary_score'] = rfm_scores.apply(lambda x: x['monetary_score'])
171 |         df_derived['rfm_score'] = rfm_scores.apply(lambda x: x['total_score'])
172 |         
173 |         # Create RFM segments
174 |         df_derived['customer_segment'] = pd.cut(
175 |             df_derived['rfm_score'],
176 |             bins=[0, 3, 6, 9],
177 |             labels=['Low Value', 'Medium Value', 'High Value']
178 |         )
179 |         
180 |         print("Added RFM scores and customer segments!")
181 |     
182 |     # Add tenure buckets
183 |     if 'tenure_months' in df_derived.columns:
184 |         df_derived['tenure_bucket'] = pd.cut(
185 |             df_derived['tenure_months'],
186 |             bins=[0, 6, 12, 24, 36, float('inf')],
187 |             labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years'],
188 |             right=False
189 |         )
190 |     
191 |     # Add days since purchase buckets
192 |     if 'days_since_last_purchase' in df_derived.columns:
193 |         df_derived['recency_bucket'] = pd.cut(
194 |             df_derived['days_since_last_purchase'],
195 |             bins=[0, 30, 60, 90, float('inf')],
196 |             labels=['0-30 days', '31-60 days', '61-90 days', 'Over 90 days'],
197 |             right=False
198 |         )
199 |     
200 |     return df_derived
201 | 
202 | # © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
203 | 
204 | def prepare_data_for_analysis(df):
205 |     """Run full data preparation pipeline for analysis"""
206 |     if df is None or df.empty:
207 |         print("No data to prepare")
208 |         return None
209 |     
210 |     # Clean data
211 |     df_clean = basic_clean(df)
212 |     
213 |     # Handle missing values
214 |     df_clean = handle_missing(df_clean)
215 |     
216 |     # Add derived features
217 |     df_clean = add_derived_features(df_clean)
218 |     
219 |     return df_clean
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
tests/smoke_tests.py

# VSCode Open Tabs
README.md,docs/SCALABLE_ARCHITECTURE.md,docs/ARCHITECTURE_DIAGRAMS.md,LICENSE,app.py,.gitignore,tests/smoke_tests.py,src/biz_metrics.py,docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md,docs/DATA_EXPLORATION_ARCHITECTURE.md,docs/IMPLEMENTATION_GUIDE.md,docs/PLAN_SUMMARY.md,docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md,docs/SEGMENTATION_IMPLEMENTATION_GUIDE.md,docs/SEGMENTATION_TECHNICAL_GUIDE.md,docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md,docs/SEGMENTATION_PLAN_SUMMARY.md,src/data_prep.py,src/eda_utils.py,src/helpers.py

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:57:15.109Z
User time zone: Asia/Calcutta, UTC+5:30

# Current Cost
$0.12

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/Users/meetjain/Downloads/InsightStream-main) Files
.gitignore
app.py
LICENSE
README.md
requirements.txt
.streamlit/
data/
data/generate_synthetic_data.py
data/sample_churn.csv
docs/
docs/CUSTOMER_SEGMENTATION_ENHANCEMENT_PLAN.md
docs/DATA_EXPLORATION_ARCHITECTURE.md
docs/DATA_EXPLORATION_ENHANCEMENT_PLAN.md
docs/IMPLEMENTATION_GUIDE.md
docs/PLAN_SUMMARY.md
docs/SCALABLE_ARCHITECTURE.md
docs/SEGMENTATION_IMPLEMENTATION_ROADMAP.md
docs/SEGMENTATION_PLAN_SUMMARY.md
docs/SEGMENTATION_TECHNICAL_GUIDE.md
models/
models/encoders_scalers/
models/encoders_scalers/num_scaler.pkl
models/encoders_scalers/ohe_encoder.pkl
notebooks/
notebooks/eda_playground.ipynb
pages/
pages/1_Data_Exploration.py
pages/2_Customer_Groups.py
pages/3_Customer_Retention.py
pages/4_Business_Insights.py
src/
src/biz_metrics.py
src/data_prep.py
src/eda_utils.py
src/helpers.py
src/sql_utils.py
tests/
tests/smoke_tests.py
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Based on my analysis of the current implementation, I'll provide comprehensive design recommendations for enhancing both the **Customer Retention & Churn Prediction Dashboard** and the **Business Insights Page** with machine learning capabilities and actionable recommendations.

## 📊 Design Analysis & Enhancement Plan

### Current State Assessment

The existing implementation provides:
- Basic churn analysis with correlation and trend visualization
- Simple business insights with ROI calculator
- RFM-based customer segmentation
- Manual risk assessment based on churn labels

### Gaps Identified

1. **No ML-based churn prediction** - Currently uses actual churn labels, not predictive models
2. **Limited risk scoring** - Binary classification (churned/not churned) vs. probability scores
3. **Basic recommendations** - Generic advice not personalized to customer segments
4. **No feature importance** - Missing ML model interpretability
5. **Limited CLV analysis** - Simplified calculation without predictive modeling

---

## 🎯 Enhanced Customer Retention & Churn Prediction Dashboard Design

### Architecture Overview

```mermaid
graph TB
    A[Customer Data] --> B[Feature Engineering]
    B --> C[ML Model Training]
    C --> D[Churn Probability Prediction]
    D --> E[Risk Segmentation]
    E --> F[Dashboard Visualization]
    
    C --> G[Feature Importance]
    G --> F
    
    D --> H[At-Risk Customer Identification]
    H --> F
    
    style C fill:#ff6b6b
    style D fill:#4ecdc4
    style F fill:#ffd166
```

### Key Components

#### 1. **ML-Powered Churn Prediction Engine**

**Recommended Models:**
- **Random Forest Classifier** - Handles non-linear relationships, provides feature importance
- **Gradient Boosting (XGBoost/LightGBM)** - High accuracy, handles imbalanced data
- **Logistic Regression** - Interpretable baseline model

**Implementation Structure:**
```python
# New file: src/churn_predictor.py
class ChurnPredictor:
    def __init__(self):
        self.model = None
        self.feature_importance = None
        self.scaler = None
        self.encoder = None
    
    def train(self, X_train, y_train):
        """Train ensemble model with cross-validation"""
        
    def predict_proba(self, X):
        """Return churn probability (0-1)"""
        
    def get_feature_importance(self):
        """Return ranked feature importance"""
        
    def explain_prediction(self, customer_data):
        """SHAP-based individual prediction explanation"""
```

#### 2. **Enhanced Risk Scoring System**

**Multi-tier Risk Bands:**
- **Critical Risk** (90-100% churn probability) - Immediate intervention
- **High Risk** (70-89%) - Urgent retention campaign
- **Medium Risk** (40-69%) - Proactive engagement
- **Low Risk** (0-39%) - Standard nurturing

**Risk Score Components:**
```python
def calculate_comprehensive_risk_score(customer):
    """
    Components:
    - ML churn probability (50%)
    - Behavioral signals (30%)
      - Days since last purchase
      - Order frequency decline
      - Support ticket volume
    - Engagement metrics (20%)
      - Email open rates
      - Website visits
      - Loyalty program activity
    """
```

#### 3. **Dashboard Layout Design**

**Tab 1: Churn Overview**
```
┌─────────────────────────────────────────────────────┐
│  📊 Churn Prediction Summary                        │
├─────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ Overall  │  │ At-Risk  │  │ Expected │         │
│  │ Churn    │  │ Customers│  │ Revenue  │         │
│  │ Rate     │  │          │  │ Loss     │         │
│  │ 23.5%    │  │   1,247  │  │ $234K    │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
│  📈 Churn Probability Distribution                  │
│  [Histogram showing customer distribution by risk]  │
│                                                     │
│  🎯 Risk Band Breakdown                             │
│  [Donut chart: Critical/High/Medium/Low]           │
└─────────────────────────────────────────────────────┘
```

**Tab 2: At-Risk Customers**
```
┌─────────────────────────────────────────────────────┐
│  🚨 High-Risk Customer List                         │
├─────────────────────────────────────────────────────┤
│  Filters: [Risk Band ▼] [Segment ▼] [Value ▼]     │
│                                                     │
│  Customer ID | Risk Score | CLV | Top Risk Factors │
│  ─────────────────────────────────────────────────  │
│  CUST001234  |    94%     |$2.3K| Low engagement   │
│  CUST005678  |    89%     |$1.8K| Payment issues   │
│  ...                                                │
│                                                     │
│  [Export List] [Create Campaign] [Bulk Actions]    │
└─────────────────────────────────────────────────────┘
```

**Tab 3: Prediction Insights**
```
┌─────────────────────────────────────────────────────┐
│  🔍 Model Performance & Feature Importance          │
├─────────────────────────────────────────────────────┤
│  Model Accuracy: 87.3% | Precision: 84.1%          │
│  Recall: 79.8% | F1-Score: 81.9%                   │
│                                                     │
│  📊 Top 10 Churn Drivers                            │
│  [Horizontal bar chart with feature importance]     │
│  1. Days since last purchase (23.4%)               │
│  2. Support tickets (18.7%)                        │
│  3. Order frequency decline (15.2%)                │
│  ...                                                │
│                                                     │
│  💡 Key Insights:                                   │
│  • Customers inactive >60 days: 3.2x churn risk    │
│  • Multiple complaints: 2.8x churn risk            │
└─────────────────────────────────────────────────────┘
```

**Tab 4: Retention Trends**
```
┌─────────────────────────────────────────────────────┐
│  📈 Churn Trends Over Time                          │
├─────────────────────────────────────────────────────┤
│  [Line chart: Predicted vs Actual churn by month]  │
│                                                     │
│  🎯 Segment-Specific Churn Rates                    │
│  [Grouped bar chart by customer segment]           │
│                                                     │
│  🔄 Cohort Analysis                                 │
│  [Heatmap: Retention rates by cohort & tenure]     │
└─────────────────────────────────────────────────────┘
```

---

## 💼 Enhanced Business Insights Page Design

### Architecture Overview

```mermaid
graph LR
    A[Customer Data] --> B[Analytics Engine]
    B --> C[Revenue Analysis]
    B --> D[CLV Prediction]
    B --> E[Retention Strategy]
    B --> F[ROI Calculator]
    
    C --> G[Recommendation Engine]
    D --> G
    E --> G
    F --> G
    
    G --> H[Plain-English Insights]
    H --> I[Actionable Reports]
    
    style G fill:#ff6b6b
    style H fill:#4ecdc4
    style I fill:#ffd166
```

### Key Components

#### 1. **AI-Powered Recommendation Engine**

**Recommendation Categories:**
```python
class RecommendationEngine:
    def generate_recommendations(self, customer_data, churn_predictions):
        """
        Returns:
        - Revenue optimization strategies
        - Retention campaign suggestions
        - Product/service improvements
        - Customer experience enhancements
        - Pricing strategy adjustments
        """
```

**Example Output:**
```
🎯 Top 3 Revenue-Boosting Actions:

1. Launch "Win-Back" Campaign for High-Risk Segment
   • Target: 347 customers with 85%+ churn probability
   • Expected ROI: 340% ($127K revenue vs $37K cost)
   • Timeline: Implement within 7 days
   • Action: 25% discount + free shipping + loyalty bonus

2. Enhance Onboarding for New Customers
   • Target: Customers in first 90 days (23% churn rate)
   • Expected Impact: Reduce early churn by 40%
   • Timeline: 30-day implementation
   • Action: Personalized welcome series + product tutorials

3. Implement Predictive Engagement for Medium-Risk
   • Target: 892 customers showing early warning signs
   • Expected ROI: 215% ($89K revenue protected)
   • Timeline: Ongoing automated campaign
   • Action: Triggered emails based on behavior patterns
```

#### 2. **Advanced CLV Analysis**

**Predictive CLV Model:**
```python
def calculate_predictive_clv(customer):
    """
    Components:
    - Historical purchase value
    - Predicted future purchases (ML-based)
    - Churn probability adjustment
    - Discount rate (time value of money)
    - Profit margin
    
    Formula:
    CLV = Σ(Predicted_Revenue_t × Survival_Probability_t × Discount_Factor_t) × Margin
    """
```

**CLV Segmentation:**
- **Platinum** (Top 5%) - CLV > $5,000
- **Gold** (Next 15%) - CLV $2,000-$5,000
- **Silver** (Next 30%) - CLV $500-$2,000
- **Bronze** (Bottom 50%) - CLV < $500

#### 3. **Dashboard Layout Design**

**Section 1: Executive Summary**
```
┌─────────────────────────────────────────────────────┐
│  💰 Revenue Impact Dashboard                        │
├─────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
│  │ At-Risk  │  │ Protected│  │ Potential│         │
│  │ Revenue  │  │ Revenue  │  │ Savings  │         │
│  │ $234K    │  │ $187K    │  │ $156K    │         │
│  └──────────┘  └──────────┘  └──────────┘         │
│                                                     │
│  📊 Revenue Breakdown by Segment                    │
│  [Stacked bar chart: At-risk vs Protected]         │
└─────────────────────────────────────────────────────┘
```

**Section 2: CLV Analysis**
```
┌─────────────────────────────────────────────────────┐
│  💎 Customer Lifetime Value Insights                │
├─────────────────────────────────────────────────────┤
│  Average CLV: $1,847 | Median CLV: $1,234          │
│                                                     │
│  📈 CLV Distribution by Segment                     │
│  [Box plot showing CLV ranges]                      │
│                                                     │
│  🎯 High-Value At-Risk Customers                    │
│  • 47 Platinum customers at risk ($235K value)     │
│  • 123 Gold customers at risk ($184K value)        │
│                                                     │
│  💡 Recommendation: Prioritize Platinum retention   │
│     campaigns - 5x ROI potential                    │
└─────────────────────────────────────────────────────┘
```

**Section 3: Retention Strategy Planner**
```
┌─────────────────────────────────────────────────────┐
│  🎯 Personalized Retention Strategies               │
├─────────────────────────────────────────────────────┤
│  Strategy Builder:                                  │
│  Target Segment: [High-Risk Platinum ▼]            │
│  Campaign Type: [Win-Back ▼]                       │
│  Budget: [$50,000]                                  │
│                                                     │
│  📊 Projected Outcomes:                             │
│  • Customers Targeted: 47                          │
│  • Expected Retention Rate: 68%                    │
│  • Revenue Protected: $159,800                     │
│  • Campaign Cost: $50,000                          │
│  • Net Benefit: $109,800                           │
│  • ROI: 220%                                        │
│                                                     │
│  📋 Recommended Actions:                            │
│  1. Personal outreach call within 48 hours         │
│  2. Exclusive 30% discount offer                   │
│  3. VIP support line access                        │
│  4. Free product upgrade                           │
│                                                     │
│  [Generate Campaign] [Export Plan] [Schedule]      │
└─────────────────────────────────────────────────────┘
```

**Section 4: Plain-English Insights**
```
┌─────────────────────────────────────────────────────┐
│  💡 What This Means for Your Business               │
├─────────────────────────────────────────────────────┤
│  🔴 Critical Issues:                                │
│  • 47 high-value customers are likely to leave     │
│    within 30 days, risking $235K in revenue        │
│  • New customer churn rate (23%) is 2x industry    │
│    average - onboarding needs improvement          │
│                                                     │
│  🟡 Opportunities:                                  │
│  • 892 medium-risk customers can be saved with     │
│    automated engagement (ROI: 215%)                │
│  • Platinum segment shows 3.2x higher CLV -        │
│    expand acquisition in this profile              │
│                                                     │
│  🟢 Strengths:                                      │
│  • Low-risk segment (67% of base) is stable        │
│  • Loyalty program members have 40% lower churn    │
│                                                     │
│  📈 Next Steps:                                     │
│  1. Launch emergency retention for 47 Platinum     │
│  2. Fix onboarding process (30-day project)        │
│  3. Automate medium-risk engagement                │
│  4. Expand Platinum customer acquisition           │
└─────────────────────────────────────────────────────┘
```

**Section 5: ROI Calculator & Scenario Planner**
```
┌─────────────────────────────────────────────────────┐
│  🧮 Interactive ROI Calculator                      │
├─────────────────────────────────────────────────────┤
│  Scenario Comparison:                               │
│                                                     │
│  ┌─────────────┬──────────┬──────────┬──────────┐ │
│  │ Scenario    │ Do       │ Targeted │ Aggressive│ │
│  │             │ Nothing  │ Campaign │ Campaign  │ │
│  ├─────────────┼──────────┼──────────┼──────────┤ │
│  │ Investment  │ $0       │ $50K     │ $150K     │ │
│  │ Retained    │ 0        │ 32       │ 89        │ │
│  │ Revenue     │ $0       │ $159K    │ $445K     │ │
│  │ Net Benefit │ -$234K   │ $109K    │ $295K     │ │
│  │ ROI         │ N/A      │ 220%     │ 197%      │ │
│  └─────────────┴──────────┴──────────┴──────────┘ │
│                                                     │
│  [Adjust Parameters] [Export Comparison]           │
└─────────────────────────────────────────────────────┘
```

---

## 🛠️ Implementation Recommendations

### Phase 1: ML Model Development (Weeks 1-2)
1. Train churn prediction models using historical data
2. Implement feature engineering pipeline
3. Validate model performance (80%+ accuracy target)
4. Deploy model inference API

### Phase 2: Dashboard Enhancement (Weeks 3-4)
1. Integrate ML predictions into retention dashboard
2. Build risk scoring visualization components
3. Create at-risk customer identification system
4. Add feature importance displays

### Phase 3: Business Insights Engine (Weeks 5-6)
1. Develop recommendation generation logic
2. Build CLV prediction model
3. Create retention strategy planner
4. Implement ROI calculator with scenarios

### Phase 4: Testing & Refinement (Week 7)
1. User acceptance testing
2. Performance optimization
3. Documentation and training materials
4. Deployment to production

---

## 📊 Key Metrics to Track

**Model Performance:**
- Prediction accuracy, precision, recall, F1-score
- AUC-ROC curve
- Calibration plots

**Business Impact:**
- Churn rate reduction
- Revenue protected
- Campaign ROI
- Customer retention rate improvement
- CLV increase

**User Engagement:**
- Dashboard usage frequency
- Report downloads
- Campaign launches from recommendations
- Time to action on insights

---

This design provides a comprehensive, ML-powered solution that transforms raw customer data into actionable business intelligence with clear, plain-English recommendations that drive measurable business outcomes.

<attempt_completion>
<result>
Comprehensive design completed for enhanced Customer Retention & Business Insights dashboards:

**Customer Retention Dashboard:**
- ML-powered churn prediction with 4-tier risk scoring (Critical/High/Medium/Low)
- At-risk customer identification with exportable lists
- Feature importance visualization showing top churn drivers
- Cohort analysis and retention trend tracking

**Business Insights Page:**
- AI-powered recommendation engine generating plain-English action plans
- Predictive CLV analysis with customer segmentation (Platinum/Gold/Silver/Bronze)
- Interactive retention strategy planner with ROI projections
- Scenario comparison tool for campaign planning
- Executive summary with critical issues, opportunities, and next steps

**Key Enhancements:**
- Random Forest/XGBoost models for churn probability prediction
- SHAP-based prediction explanations
- Automated retention campaign suggestions
- Revenue impact quantification
- Multi-scenario ROI calculator

**Implementation:** 7-week phased approach covering ML development, dashboard integration, business logic, and testing.

All designs include detailed architecture diagrams, component specifications, and UI mockups ready for development.
</result>
</attempt_completion>

