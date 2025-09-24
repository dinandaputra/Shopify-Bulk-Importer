# Reporting Scripts

Scripts for generating reports and analytics from Shopify data.

## Purpose

Reporting scripts provide insights through:
- Sales analytics
- Inventory reports  
- Product performance metrics
- Missing data reports
- Trend analysis
- Export for external analysis

## Common Report Types

### Inventory Report
Generate comprehensive inventory status:

```python
def generate_inventory_report():
    """Generate inventory report across all products"""
    
    api = ShopifyAPI()
    products = api.get_all_products()
    
    report = {
        'generated_at': datetime.now().isoformat(),
        'summary': {
            'total_products': 0,
            'total_variants': 0,
            'total_inventory': 0,
            'out_of_stock': 0,
            'low_stock': 0
        },
        'products': []
    }
    
    for product in products:
        product_data = {
            'title': product['title'],
            'handle': product['handle'],
            'variants': []
        }
        
        for variant in product['variants']:
            quantity = variant.get('inventory_quantity', 0)
            
            variant_data = {
                'sku': variant.get('sku'),
                'price': variant['price'],
                'inventory': quantity,
                'status': get_stock_status(quantity)
            }
            
            product_data['variants'].append(variant_data)
            
            # Update summary
            report['summary']['total_variants'] += 1
            report['summary']['total_inventory'] += quantity
            
            if quantity == 0:
                report['summary']['out_of_stock'] += 1
            elif quantity < 10:
                report['summary']['low_stock'] += 1
        
        report['products'].append(product_data)
        report['summary']['total_products'] += 1
    
    return report

def get_stock_status(quantity):
    """Determine stock status"""
    if quantity == 0:
        return 'out_of_stock'
    elif quantity < 10:
        return 'low_stock'
    else:
        return 'in_stock'
```

### Sales Performance Report
Analyze product sales performance:

```python
def generate_sales_report(start_date, end_date):
    """Generate sales performance report"""
    
    api = ShopifyAPI()
    
    # Get orders in date range
    orders = api.get_orders(
        created_at_min=start_date,
        created_at_max=end_date
    )
    
    # Aggregate sales data
    product_sales = {}
    
    for order in orders:
        for line_item in order['line_items']:
            product_id = line_item['product_id']
            
            if product_id not in product_sales:
                product_sales[product_id] = {
                    'title': line_item['title'],
                    'quantity_sold': 0,
                    'revenue': 0,
                    'orders': 0
                }
            
            product_sales[product_id]['quantity_sold'] += line_item['quantity']
            product_sales[product_id]['revenue'] += float(line_item['price']) * line_item['quantity']
            product_sales[product_id]['orders'] += 1
    
    # Sort by revenue
    sorted_products = sorted(
        product_sales.items(),
        key=lambda x: x[1]['revenue'],
        reverse=True
    )
    
    return {
        'period': {
            'start': start_date,
            'end': end_date
        },
        'summary': {
            'total_products_sold': len(product_sales),
            'total_revenue': sum(p['revenue'] for p in product_sales.values()),
            'total_units_sold': sum(p['quantity_sold'] for p in product_sales.values())
        },
        'top_products': sorted_products[:20]
    }
```

### Missing Data Report
Identify products with incomplete data:

```python
def generate_missing_data_report():
    """Find products with missing required fields"""
    
    api = ShopifyAPI()
    products = api.get_all_products()
    
    missing_data = {
        'no_images': [],
        'no_description': [],
        'no_metafields': [],
        'no_sku': [],
        'no_weight': []
    }
    
    for product in products:
        # Check images
        if not product.get('images'):
            missing_data['no_images'].append({
                'id': product['id'],
                'title': product['title'],
                'handle': product['handle']
            })
        
        # Check description
        if not product.get('body_html'):
            missing_data['no_description'].append({
                'id': product['id'],
                'title': product['title']
            })
        
        # Check metafields
        metafields = api.get_product_metafields(product['id'])
        if not metafields:
            missing_data['no_metafields'].append({
                'id': product['id'],
                'title': product['title']
            })
        
        # Check variants
        for variant in product['variants']:
            if not variant.get('sku'):
                missing_data['no_sku'].append({
                    'product': product['title'],
                    'variant_id': variant['id']
                })
            
            if not variant.get('weight'):
                missing_data['no_weight'].append({
                    'product': product['title'],
                    'variant_id': variant['id']
                })
    
    return missing_data
```

## Report Formatting

### HTML Report Generation
Create formatted HTML reports:

```python
def generate_html_report(data, template='default'):
    """Generate HTML report from data"""
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{data['title']}</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #4CAF50; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            .summary {{ background-color: #e7f3fe; padding: 15px; margin-bottom: 20px; }}
            .metric {{ display: inline-block; margin: 10px 20px; }}
            .metric-value {{ font-size: 24px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>{data['title']}</h1>
        <div class="summary">
            {generate_summary_html(data['summary'])}
        </div>
        {generate_table_html(data['details'])}
    </body>
    </html>
    """
    
    return html

def generate_summary_html(summary):
    """Generate summary metrics HTML"""
    metrics_html = ""
    
    for key, value in summary.items():
        metrics_html += f"""
        <div class="metric">
            <div class="metric-label">{key.replace('_', ' ').title()}</div>
            <div class="metric-value">{value:,}</div>
        </div>
        """
    
    return metrics_html
```

### CSV Export
Export reports to CSV:

```python
def export_report_to_csv(report_data, filename):
    """Export report data to CSV file"""
    
    import csv
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        if isinstance(report_data, list) and report_data:
            # List of dictionaries
            writer = csv.DictWriter(f, fieldnames=report_data[0].keys())
            writer.writeheader()
            writer.writerows(report_data)
            
        elif isinstance(report_data, dict):
            # Dictionary with nested data
            # Flatten for CSV
            rows = []
            for key, value in report_data.items():
                if isinstance(value, list):
                    for item in value:
                        row = {'category': key}
                        row.update(item)
                        rows.append(row)
                else:
                    rows.append({'category': key, 'value': value})
            
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
    
    print(f"Report exported to {filename}")
```

### Dashboard View
Create dashboard-style reports:

```python
def generate_dashboard_report():
    """Generate comprehensive dashboard report"""
    
    dashboard = {
        'generated_at': datetime.now().isoformat(),
        'metrics': {},
        'charts': {},
        'alerts': []
    }
    
    # Key metrics
    dashboard['metrics'] = {
        'total_products': get_product_count(),
        'total_inventory_value': get_inventory_value(),
        'low_stock_items': get_low_stock_count(),
        'products_without_images': get_products_without_images_count()
    }
    
    # Chart data
    dashboard['charts'] = {
        'inventory_by_category': get_inventory_by_category(),
        'price_distribution': get_price_distribution(),
        'stock_levels': get_stock_level_distribution()
    }
    
    # Alerts
    if dashboard['metrics']['low_stock_items'] > 10:
        dashboard['alerts'].append({
            'type': 'warning',
            'message': f"{dashboard['metrics']['low_stock_items']} items are low on stock"
        })
    
    return dashboard
```

## Scheduling Reports

### Automated Report Generation
Set up scheduled reports:

```python
def schedule_daily_reports():
    """Schedule daily report generation"""
    
    import schedule
    import time
    
    def run_daily_reports():
        print(f"Running daily reports at {datetime.now()}")
        
        # Generate reports
        inventory_report = generate_inventory_report()
        save_report(inventory_report, 'inventory')
        
        sales_report = generate_sales_report(
            start_date=datetime.now() - timedelta(days=1),
            end_date=datetime.now()
        )
        save_report(sales_report, 'daily_sales')
        
        # Email reports
        email_reports([inventory_report, sales_report])
    
    # Schedule
    schedule.every().day.at("09:00").do(run_daily_reports)
    
    # Run scheduler
    while True:
        schedule.run_pending()
        time.sleep(60)
```

## Best Practices

1. **Cache data** - Don't repeatedly fetch the same data
2. **Use pagination** - Handle large datasets properly
3. **Add timestamps** - Always include generation time
4. **Version reports** - Track report format changes
5. **Handle errors gracefully** - Don't crash on bad data
6. **Optimize queries** - Use GraphQL for efficiency
7. **Archive old reports** - Keep historical data
8. **Make reports actionable** - Include recommendations

## Example: Complete Inventory Analysis Report

```python
#!/usr/bin/env python3
"""
Generate comprehensive inventory analysis report
"""

import json
from datetime import datetime
from collections import defaultdict
from services.shopify_api import ShopifyAPI

class InventoryAnalysisReport:
    def __init__(self):
        self.api = ShopifyAPI()
        self.report_data = {
            'generated_at': datetime.now().isoformat(),
            'store': self.api.shop_domain,
            'analysis': {}
        }
    
    def generate(self):
        """Generate complete inventory analysis"""
        print("Fetching product data...")
        products = self.api.get_all_products()
        
        print("Analyzing inventory...")
        self.analyze_stock_levels(products)
        self.analyze_by_category(products)
        self.analyze_value(products)
        self.find_issues(products)
        
        print("Generating recommendations...")
        self.generate_recommendations()
        
        return self.report_data
    
    def analyze_stock_levels(self, products):
        """Analyze stock levels across products"""
        stock_analysis = {
            'total_skus': 0,
            'in_stock': 0,
            'low_stock': 0,
            'out_of_stock': 0,
            'stock_distribution': defaultdict(int)
        }
        
        for product in products:
            for variant in product['variants']:
                quantity = variant.get('inventory_quantity', 0)
                stock_analysis['total_skus'] += 1
                
                if quantity == 0:
                    stock_analysis['out_of_stock'] += 1
                elif quantity < 10:
                    stock_analysis['low_stock'] += 1
                else:
                    stock_analysis['in_stock'] += 1
                
                # Distribution buckets
                if quantity == 0:
                    bucket = '0'
                elif quantity < 10:
                    bucket = '1-9'
                elif quantity < 50:
                    bucket = '10-49'
                elif quantity < 100:
                    bucket = '50-99'
                else:
                    bucket = '100+'
                
                stock_analysis['stock_distribution'][bucket] += 1
        
        self.report_data['analysis']['stock_levels'] = stock_analysis
    
    def analyze_by_category(self, products):
        """Analyze inventory by product category"""
        category_analysis = defaultdict(lambda: {
            'products': 0,
            'variants': 0,
            'total_stock': 0,
            'total_value': 0
        })
        
        for product in products:
            category = product.get('product_type', 'Uncategorized')
            category_analysis[category]['products'] += 1
            
            for variant in product['variants']:
                category_analysis[category]['variants'] += 1
                quantity = variant.get('inventory_quantity', 0)
                price = float(variant.get('price', 0))
                
                category_analysis[category]['total_stock'] += quantity
                category_analysis[category]['total_value'] += quantity * price
        
        self.report_data['analysis']['by_category'] = dict(category_analysis)
    
    def analyze_value(self, products):
        """Analyze inventory value"""
        value_analysis = {
            'total_inventory_value': 0,
            'average_product_value': 0,
            'highest_value_items': [],
            'lowest_value_items': []
        }
        
        product_values = []
        
        for product in products:
            product_value = 0
            
            for variant in product['variants']:
                quantity = variant.get('inventory_quantity', 0)
                price = float(variant.get('price', 0))
                product_value += quantity * price
            
            if product_value > 0:
                product_values.append({
                    'title': product['title'],
                    'handle': product['handle'],
                    'value': product_value
                })
                value_analysis['total_inventory_value'] += product_value
        
        # Sort and get top/bottom items
        product_values.sort(key=lambda x: x['value'], reverse=True)
        value_analysis['highest_value_items'] = product_values[:10]
        value_analysis['lowest_value_items'] = product_values[-10:]
        
        if product_values:
            value_analysis['average_product_value'] = (
                value_analysis['total_inventory_value'] / len(product_values)
            )
        
        self.report_data['analysis']['value'] = value_analysis
    
    def find_issues(self, products):
        """Find inventory issues"""
        issues = {
            'negative_inventory': [],
            'no_sku': [],
            'duplicate_skus': defaultdict(list),
            'no_tracking': []
        }
        
        seen_skus = {}
        
        for product in products:
            for variant in product['variants']:
                # Negative inventory
                if variant.get('inventory_quantity', 0) < 0:
                    issues['negative_inventory'].append({
                        'product': product['title'],
                        'variant': variant.get('title'),
                        'quantity': variant['inventory_quantity']
                    })
                
                # Missing SKU
                sku = variant.get('sku')
                if not sku:
                    issues['no_sku'].append({
                        'product': product['title'],
                        'variant_id': variant['id']
                    })
                elif sku in seen_skus:
                    # Duplicate SKU
                    issues['duplicate_skus'][sku].append({
                        'product': product['title'],
                        'variant_id': variant['id']
                    })
                else:
                    seen_skus[sku] = product['title']
                
                # No inventory tracking
                if variant.get('inventory_management') != 'shopify':
                    issues['no_tracking'].append({
                        'product': product['title'],
                        'variant': variant.get('title')
                    })
        
        self.report_data['analysis']['issues'] = dict(issues)
    
    def generate_recommendations(self):
        """Generate actionable recommendations"""
        recommendations = []
        analysis = self.report_data['analysis']
        
        # Stock level recommendations
        stock = analysis['stock_levels']
        if stock['out_of_stock'] > stock['total_skus'] * 0.1:
            recommendations.append({
                'priority': 'high',
                'type': 'restock',
                'message': f"{stock['out_of_stock']} SKUs are out of stock (>10% of total)",
                'action': 'Review and reorder out-of-stock items'
            })
        
        if stock['low_stock'] > stock['total_skus'] * 0.2:
            recommendations.append({
                'priority': 'medium',
                'type': 'restock',
                'message': f"{stock['low_stock']} SKUs have low stock levels",
                'action': 'Plan reorders for low stock items'
            })
        
        # Issue recommendations
        issues = analysis['issues']
        if issues['duplicate_skus']:
            recommendations.append({
                'priority': 'high',
                'type': 'data_quality',
                'message': f"Found {len(issues['duplicate_skus'])} duplicate SKUs",
                'action': 'Review and fix duplicate SKUs'
            })
        
        if len(issues['no_sku']) > 10:
            recommendations.append({
                'priority': 'medium',
                'type': 'data_quality',
                'message': f"{len(issues['no_sku'])} variants have no SKU",
                'action': 'Assign SKUs to all variants'
            })
        
        self.report_data['recommendations'] = recommendations
    
    def save(self, format='json'):
        """Save report to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format == 'json':
            filename = f'inventory_analysis_{timestamp}.json'
            with open(filename, 'w') as f:
                json.dump(self.report_data, f, indent=2)
        
        elif format == 'html':
            filename = f'inventory_analysis_{timestamp}.html'
            html = generate_html_report(self.report_data)
            with open(filename, 'w') as f:
                f.write(html)
        
        print(f"Report saved to {filename}")
        return filename

if __name__ == "__main__":
    report = InventoryAnalysisReport()
    report_data = report.generate()
    report.save('json')
    report.save('html')
```