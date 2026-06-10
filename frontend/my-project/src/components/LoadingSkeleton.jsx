export default function LoadingSkeleton() {
    return (
        <div className="loading-skeleton">
            <div className="skeleton-header" />
            <div className="skeleton-grid">
                {Array.from({ length: 4 }).map((_, index) => (
                    <div key={index} className="skeleton-card" />
                ))}
            </div>
            <div className="skeleton-table" />
        </div>
    )
}
