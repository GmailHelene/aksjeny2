from flask import render_template
from app import app
from app.utils import get_sector_data, generate_demo_sectors

@app.route('/market-intel/sector-analysis')
def sector_analysis():
    try:
        # Get real sector data
        sectors = get_sector_data()
        if not sectors:
            sectors = generate_demo_sectors()
        return render_template('market-intel/sector-analysis.html', 
                             sectors=sectors,
                             error=False)
    except Exception as e:
        app.logger.error(f"Sector analysis error: {str(e)}")
        return render_template('market-intel/sector-analysis.html', 
                             sectors=[],
                             error=True)