"""
Business metrics for customer churn prediction app.
"""
import pandas as pd
import numpy as np

from .helpers import COST_RETAIN, AVG_FUTURE_ORDERS

def calculate_revenue_impact(df, churn_prob_col, avg_order_value_col):
    """
    Calculate the expected revenue impact of churn
    """
    if df is None or df.empty:
        return {
            'error': "No data provided for revenue impact calculation."
        }
    
    if churn_prob_col not in df.columns:
        return {
            'error': f"Churn probability column '{churn_prob_col}' not found in data."
        }
    
    if avg_order_value_col not in df.columns:
        return {
            'error': f"Average order value column '{avg_order_value_col}' not found in data."
        }
    
    try:
        # Total customers
        total_customers = len(df)
        
        # Expected number of churners
        expected_churners = df[churn_prob_col].sum()
        expected_churn_rate = expected_churners / total_customers * 100
        
        # Expected revenue loss
        avg_order_value = df[avg_order_value_col].mean()
        expected_revenue_loss = expected_churners * avg_order_value * AVG_FUTURE_ORDERS
        
        # Per customer metrics
        avg_expected_loss_per_customer = expected_revenue_loss / total_customers
        
        # Results
        results = {
            'total_customers': total_customers,
            'expected_churners': expected_churners,
            'expected_churn_rate': expected_churn_rate,
            'avg_order_value': avg_order_value,
            'expected_revenue_loss': expected_revenue_loss,
            'avg_expected_loss_per_customer': avg_expected_loss_per_customer
        }
        
        return results
    
    except Exception as e:
        print(f"Error calculating revenue impact: {e}")
        return {
            'error': f"Revenue impact calculation failed: {str(e)}"
        }

def calculate_targeting_roi(df, churn_prob_col, avg_order_value_col, risk_band_col=None):
    """
    Calculate ROI for targeting different risk segments
    """
    if df is None or df.empty:
        return {
            'error': "No data provided for ROI calculation."
        }
    
    if churn_prob_col not in df.columns:
        return {
            'error': f"Churn probability column '{churn_prob_col}' not found in data."
        }
    
    if avg_order_value_col not in df.columns:
        return {
            'error': f"Average order value column '{avg_order_value_col}' not found in data."
        }
    
    try:
        # Make a copy of the data
        df_calc = df.copy()
        
        # Sort by churn probability (descending)
        df_calc = df_calc.sort_values(churn_prob_col, ascending=False)
        
        # Calculate potential loss per customer
        df_calc['potential_loss'] = df_calc[avg_order_value_col] * AVG_FUTURE_ORDERS
        
        # Calculate expected loss (probability × potential loss)
        df_calc['expected_loss'] = df_calc[churn_prob_col] * df_calc['potential_loss']
        
        # Calculate retention cost
        df_calc['retention_cost'] = COST_RETAIN
        
        # Calculate expected benefit (expected loss - retention cost)
        df_calc['expected_benefit'] = df_calc['expected_loss'] - df_calc['retention_cost']
        
        # Calculate cumulative metrics at different targeting thresholds
        results = []
        
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.
        
        # Calculate total expected loss
        total_expected_loss = df_calc['expected_loss'].sum()
        
        # Get risk bands if available
        has_risk_bands = risk_band_col in df_calc.columns
        
        if has_risk_bands:
            # Calculate metrics for each risk band
            for band in ['High Risk', 'Medium Risk', 'Low Risk']:
                band_df = df_calc[df_calc[risk_band_col] == band]
                
                if len(band_df) == 0:
                    continue
                
                customers_count = len(band_df)
                total_retention_cost = customers_count * COST_RETAIN
                expected_loss_saved = band_df['expected_loss'].sum()
                expected_benefit = expected_loss_saved - total_retention_cost
                percentage_targeted = customers_count / len(df_calc) * 100
                
                results.append({
                    'segment': band,
                    'customers_count': customers_count,
                    'percentage_targeted': percentage_targeted,
                    'total_retention_cost': total_retention_cost,
                    'expected_loss_saved': expected_loss_saved,
                    'expected_benefit': expected_benefit,
                    'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0
                })
        
        # Calculate metrics for different targeting percentages
        percentiles = range(10, 101, 10)
        
        for p in percentiles:
            cutoff_idx = int(len(df_calc) * p / 100)
            targeted_df = df_calc.iloc[:cutoff_idx]
            
            customers_count = len(targeted_df)
            total_retention_cost = customers_count * COST_RETAIN
            expected_loss_saved = targeted_df['expected_loss'].sum()
            expected_benefit = expected_loss_saved - total_retention_cost
            
            results.append({
                'segment': f"Top {p}%",
                'customers_count': customers_count,
                'percentage_targeted': p,
                'total_retention_cost': total_retention_cost,
                'expected_loss_saved': expected_loss_saved,
                'expected_benefit': expected_benefit,
                'roi_ratio': expected_loss_saved / total_retention_cost if total_retention_cost > 0 else 0,
                'percent_of_total_loss': expected_loss_saved / total_expected_loss * 100 if total_expected_loss > 0 else 0
            })
        
        return {
            'by_segment': results,
            'total_expected_loss': total_expected_loss
        }
    
    except Exception as e:
        print(f"Error calculating targeting ROI: {e}")
        return {
            'error': f"ROI calculation failed: {str(e)}"
        }
    
# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.


def get_retention_playbook_by_risk(risk_band):
    """
    Get retention playbook recommendations based on risk band
    """
    if risk_band == "High Risk":
        actions = [
            "Send personalized email with 20% discount coupon valid for 7 days",
            "Follow up with a phone call from customer service within 48 hours",
            "Offer free expedited shipping on next order",
            "Add loyalty points boost (2x points for next 30 days)",
            "Invite to exclusive product preview or early access"
        ]
    elif risk_band == "Medium Risk":
        actions = [
            "Send email with 10% discount coupon valid for 14 days",
            "Recommend products based on previous purchases",
            "Send reminder about loyalty points balance and upcoming expiration",
            "Share new product announcements in their favorite categories",
            "Ask for feedback or product review with small incentive"
        ]
    else:  # Low Risk
        actions = [
            "Include in regular marketing newsletters",
            "Maintain standard loyalty program communications",
            "Periodic engagement with seasonal promotions",
            "Anniversary or birthday special offers",
            "Invite to refer friends with dual incentives"
        ]
    
    return actions

def get_targeting_recommendations(roi_results):
    """
    Get recommendations based on ROI calculations
    """
    if 'error' in roi_results:
        return [
            "Couldn't calculate targeting recommendations due to an error.",
            "Please ensure your data includes churn probabilities and order values."
        ]
    
    recommendations = []
    
    # Get segment data
    segments = roi_results.get('by_segment', [])
    total_expected_loss = roi_results.get('total_expected_loss', 0)
    
    # Find best ROI segment
    best_roi_segment = None
    best_roi = 0
    
    for segment in segments:
        if segment['roi_ratio'] > best_roi:
            best_roi = segment['roi_ratio']
            best_roi_segment = segment
    
    if best_roi_segment:
        if 'High Risk' in best_roi_segment.get('segment', ''):
            recommendations.append(
                f"Focus on High Risk customers first - each $1 spent on retention saves ${best_roi:.2f} in revenue!"
            )
        elif 'Top' in best_roi_segment.get('segment', ''):
            recommendations.append(
                f"Target the {best_roi_segment['segment']} of customers for best ROI - each $1 spent saves ${best_roi:.2f}!"
            )
    
    # Find optimal targeting percentage
    optimal_segment = None
    max_benefit = 0
    
    for segment in segments:
        if 'Top' in segment.get('segment', '') and segment['expected_benefit'] > max_benefit:
            max_benefit = segment['expected_benefit']
            optimal_segment = segment
    
    if optimal_segment:
        recommendations.append(
            f"Optimal targeting strategy: {optimal_segment['segment']} of customers (saves ${optimal_segment['expected_benefit']:.2f})"
        )
    
    # Add general recommendations
    recommendations.extend([
        f"Total expected loss from churn: ${total_expected_loss:.2f} - this is what we're trying to prevent!",
        "Customize retention offers based on customer value and risk level for best results",
        "Track campaign performance and adjust targeting thresholds over time"
    ])
    
    return recommendations

def generate_business_report(df, churn_predictions, feature_importance, cost_benefit_df=None):
    """
    Generate a business report with insights and recommendations
    """
    if df is None or df.empty:
        return "No data available for business report."
    
    # Calculate basic metrics
    total_customers = len(df)
    churn_rate = df['churn'].mean() * 100 if 'churn' in df.columns else None
    
    # Start building the report
    report = "# Customer Churn Business Report\n\n"
    
    # Current situation
    report += "## Current Situation\n\n"
    
    if churn_rate is not None:
        report += f"- Current churn rate: **{churn_rate:.1f}%** of customers\n"
    
    # Get average order value and tenure
    avg_order = df['avg_order_value'].mean() if 'avg_order_value' in df.columns else None
    avg_tenure = df['tenure_months'].mean() if 'tenure_months' in df.columns else None
    
    if avg_order is not None:
        report += f"- Average order value: **${avg_order:.2f}**\n"
    
    if avg_tenure is not None:
        report += f"- Average customer tenure: **{avg_tenure:.1f} months**\n"
    
    # Risky segments
    report += "\n## High-Risk Customer Segments\n\n"
    
    # By region if available
    if 'region' in df.columns:
        churn_by_region = df.groupby('region')['churn'].mean().sort_values(ascending=False)
        highest_region = churn_by_region.index[0]
        highest_region_rate = churn_by_region.iloc[0] * 100
        
        report += f"- **{highest_region} region** has highest churn rate at {highest_region_rate:.1f}%\n"
    
    # By payment type if available
    if 'payment_type' in df.columns:
        churn_by_payment = df.groupby('payment_type')['churn'].mean().sort_values(ascending=False)
        highest_payment = churn_by_payment.index[0]
        highest_payment_rate = churn_by_payment.iloc[0] * 100
        
        report += f"- **{highest_payment} payment** users churn at {highest_payment_rate:.1f}%\n"
    
    # By tenure buckets if available
    if 'tenure_months' in df.columns:
        df['tenure_bucket'] = pd.cut(
            df['tenure_months'], 
            bins=[0, 6, 12, 24, 36, float('inf')],
            labels=['0-6 months', '7-12 months', '1-2 years', '2-3 years', '3+ years']
        )
        churn_by_tenure = df.groupby('tenure_bucket')['churn'].mean().sort_values(ascending=False)
        highest_tenure = churn_by_tenure.index[0]
        highest_tenure_rate = churn_by_tenure.iloc[0] * 100
        
        report += f"- Customers in **{highest_tenure}** tenure bracket churn at {highest_tenure_rate:.1f}%\n"
    
    # Key drivers section
    report += "\n## Top 5 Churn Drivers\n\n"
    
    # Use feature importance if available
    if feature_importance and len(feature_importance) > 0:
        for i, feature in enumerate(feature_importance[:5], 1):
            name = feature.get('feature', '')
            explanation = feature.get('explanation', '')
            
            report += f"{i}. **{name}**: {explanation}\n"
    else:
        report += "Feature importance data not available.\n"

# © 2026 | Project created by Meet Jain(@Meetjain1) and  Aditi Gopinath(@aaditiiiii1). Unauthorized copying or reproduction is prohibited.

    # Targeting plan
    report += "\n## Targeting Plan\n\n"
    
    if cost_benefit_df is not None and not cost_benefit_df.empty:
        # Find optimal targeting percentage
        optimal_row = cost_benefit_df.loc[cost_benefit_df['net_benefit'].idxmax()]
        optimal_percent = optimal_row['targeting_percent']
        optimal_benefit = optimal_row['net_benefit']
        optimal_customers = optimal_row['customers_targeted']
        optimal_churners = optimal_row['churners_caught']
        optimal_churners_pct = optimal_row['churners_caught_percent']
        
        report += f"- **Optimal strategy**: Target top {optimal_percent:.0f}% highest-risk customers\n"
        report += f"- This means focusing on **{optimal_customers:.0f} customers**\n"
        report += f"- Expected to save **${optimal_benefit:.2f}** in revenue\n"
        report += f"- Would catch **{optimal_churners:.0f} churners** ({optimal_churners_pct:.1f}% of all churners)\n"
    else:
        report += "Cost-benefit analysis data not available.\n"
    
    # Action items
    report += "\n## Recommended Actions\n\n"
    
    # High risk actions
    report += "### For High-Risk Customers:\n"
    report += "1. Send personalized email with 20% discount coupon valid for 7 days\n"
    report += "2. Follow up with a phone call from customer service within 48 hours\n"
    report += "3. Offer free expedited shipping on next order\n"
    
    # Medium risk actions
    report += "\n### For Medium-Risk Customers:\n"
    report += "1. Send email with 10% discount coupon valid for 14 days\n"
    report += "2. Recommend products based on previous purchases\n"
    report += "3. Send reminder about loyalty points balance\n"
    
    # Product/service improvements
    report += "\n### Product/Service Improvements:\n"
    
    # Look at complaints if available
    if 'complaints' in df.columns and df['complaints'].sum() > 0:
        report += "1. Address common customer complaints to improve retention\n"
    else:
        report += "1. Review customer feedback for product improvement opportunities\n"
    
    report += "2. Consider loyalty program adjustments for better engagement\n"
    report += "3. Improve onboarding for new customers (first 6 months critical)\n"
    
    # 30-day roadmap
    report += "\n## Next 30 Days Roadmap\n\n"
    report += "1. **Week 1**: Launch high-risk customer retention campaign\n"
    report += "2. **Week 2**: Begin medium-risk customer engagement\n"
    report += "3. **Week 3**: Analyze initial campaign results and adjust\n"
    report += "4. **Week 4**: Prepare follow-up actions and long-term strategy\n"
    
    # Final notes
    report += "\n## Notes\n\n"
    report += "- This is an initial analysis based on available data\n"
    report += "- Campaign effectiveness should be measured and tactics adjusted\n"
    report += "- Consider A/B testing different retention offers\n"
    report += "- Long-term product/service improvements will have most sustainable impact\n"
    
    return report
