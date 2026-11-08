#!/usr/bin/env python3
"""
IPRoyal Residential & Datacenter Proxy TCO Cost Calculator
Models bandwidth costs, volume tier discounts, and monthly savings vs legacy providers.
"""

import sys

def calculate_iproyal_tco(bandwidth_gb: float, proxy_type: str = "residential", promo_discount: float = 0.05):
    rates = {
        "residential": [
            (1, 3.95),
            (10, 3.80),
            (50, 3.50),
            (100, 3.15),
            (250, 2.80),
            (500, 2.45),
            (1000, 2.10),
            (2500, 1.75)
        ],
        "datacenter_per_ip": 1.57,
        "dedicated_isp": 2.40
    }
    
    if proxy_type == "residential":
        unit_rate = 3.95
        for threshold, rate in rates["residential"]:
            if bandwidth_gb >= threshold:
                unit_rate = rate
        base_cost = bandwidth_gb * unit_rate
        net_cost = base_cost * (1.0 - promo_discount)
        brightdata_equiv = bandwidth_gb * 8.40
        smartproxy_equiv = bandwidth_gb * 4.50
        return {
            "bandwidth_gb": bandwidth_gb,
            "unit_rate_usd": unit_rate,
            "net_cost_usd": round(net_cost, 2),
            "brightdata_cost_usd": round(brightdata_equiv, 2),
            "smartproxy_cost_usd": round(smartproxy_equiv, 2),
            "savings_vs_brightdata": round(brightdata_equiv - net_cost, 2),
            "savings_vs_smartproxy": round(smartproxy_equiv - net_cost, 2)
        }
    else:
        count = bandwidth_gb
        cost = count * rates.get(proxy_type, 1.57) * (1.0 - promo_discount)
        return {"units": count, "net_cost_usd": round(cost, 2)}

if __name__ == "__main__":
    gb = float(sys.argv[1]) if len(sys.argv) > 1 else 100.0
    res = calculate_iproyal_tco(gb)
    print(f"=== IPRoyal TCO Calculation for {res['bandwidth_gb']} GB ===")
    print(f"Unit Rate: ${res['unit_rate_usd']}/GB")
    print(f"IPRoyal Total: ${res['net_cost_usd']}")
    print(f"Bright Data Equivalent: ${res['brightdata_cost_usd']} (Save ${res['savings_vs_brightdata']})")
    print(f"Smartproxy Equivalent: ${res['smartproxy_cost_usd']} (Save ${res['savings_vs_smartproxy']})")
