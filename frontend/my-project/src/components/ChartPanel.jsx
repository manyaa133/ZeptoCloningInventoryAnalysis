import {
    Bar,
    BarChart,
    CartesianGrid,
    Cell,
    Legend,
    Pie,
    PieChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts'

const CHART_COLORS = ['#8b5cf6', '#a855f7', '#f472b6', '#facc15', '#22c55e', '#38bdf8']

export default function ChartPanel({ categoryDistribution, valueByCategory }) {
    return (
        <section className="chart-panel">
            <div className="chart-card">
                <div className="chart-card-header">
                    <h3>Category Distribution</h3>
                </div>
                <ResponsiveContainer width="100%" height={260}>
                    <PieChart>
                        <Pie
                            data={categoryDistribution}
                            dataKey="count"
                            nameKey="category"
                            outerRadius={96}
                            fill="#8884d8"
                            label
                        >
                            {categoryDistribution.map((entry, index) => (
                                <Cell key={entry.category} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                            ))}
                        </Pie>
                        <Tooltip />
                        <Legend verticalAlign="bottom" height={44} />
                    </PieChart>
                </ResponsiveContainer>
            </div>

            <div className="chart-card">
                <div className="chart-card-header">
                    <h3>Inventory Value by Category</h3>
                </div>
                <ResponsiveContainer width="100%" height={260}>
                    <BarChart data={valueByCategory} margin={{ top: 20, right: 18, left: -8, bottom: 10 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.08)" />
                        <XAxis dataKey="category" tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                        <YAxis tick={{ fill: 'var(--text-muted)', fontSize: 12 }} />
                        <Tooltip formatter={(value) => [`$${value.toLocaleString()}`, 'Value']} />
                        <Bar dataKey="value" fill="#8b5cf6" radius={[8, 8, 0, 0]} />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </section>
    )
}
