/**
 * Interactive Client-Side Visualizations using Chart.js
 */
function initResultCharts(planData) {
  if (typeof Chart === 'undefined') return;

  // 1. Macronutrient Calorie Breakdown (Doughnut)
  const macroCtx = document.getElementById('macroDoughnutChart');
  if (macroCtx && planData) {
    new Chart(macroCtx, {
      type: 'doughnut',
      data: {
        labels: ['Protein (' + planData.protein + 'g)', 'Carbs (' + planData.carbs + 'g)', 'Fat (' + planData.fat + 'g)'],
        datasets: [{
          data: [planData.protein_calories, planData.carbs_calories, planData.fat_calories],
          backgroundColor: ['#6366f1', '#06b6d4', '#ec4899'],
          borderWidth: 0,
          hoverOffset: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'bottom',
            labels: { color: '#94a3b8', font: { family: 'Outfit', size: 12 } }
          },
          tooltip: {
            callbacks: {
              label: function(ctx) {
                return ` ${ctx.label}: ${ctx.raw} kcal (${Math.round(ctx.raw / planData.calories * 100)}%)`;
              }
            }
          }
        },
        cutout: '70%'
      }
    });
  }

  // 2. Caloric Energy Baseline vs ML Target (Bar Chart)
  const calorieCtx = document.getElementById('energyComparisonChart');
  if (calorieCtx && planData) {
    new Chart(calorieCtx, {
      type: 'bar',
      data: {
        labels: ['BMR Baseline', 'TDEE Maintenance', 'AI Tailored Target'],
        datasets: [{
          label: 'Energy (kcal/day)',
          data: [planData.bmr || (planData.tdee_baseline * 0.7), planData.tdee_baseline, planData.calories],
          backgroundColor: ['#94a3b8', '#3b82f6', '#10b981'],
          borderRadius: 8
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              label: (ctx) => ` ${ctx.raw} kcal/day`
            }
          }
        },
        scales: {
          y: {
            grid: { color: 'rgba(255, 255, 255, 0.06)' },
            ticks: { color: '#94a3b8' }
          },
          x: {
            grid: { display: false },
            ticks: { color: '#94a3b8' }
          }
        }
      }
    });
  }
}
