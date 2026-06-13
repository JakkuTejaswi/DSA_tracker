import React, { useEffect, useState, useMemo } from "react";
import API from "../services/api";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [readiness, setReadiness] = useState(null);
  const [problems, setProblems] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [hasMore, setHasMore] = useState(true);
  const [searchTerm, setSearchTerm] = useState("");
  const [filterTopic, setFilterTopic] = useState("");
  
  const navigate = useNavigate();
  const limit = 50;

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem("token");
      if (!token) {
        navigate("/");
        return;
      }
      try {
        const [statsRes, readinessRes, recRes] = await Promise.all([
          API.get("/analytics/dashboard"),
          API.get("/ml/readiness"),
          API.get("/problems/recommendations")
        ]);
        setStats(statsRes.data);
        setReadiness(readinessRes.data.interview_readiness_score);
        setRecommendations(recRes.data);
      } catch (err) {
        console.error("Error fetching dashboard data", err);
      }
    };
    fetchData();
  }, [navigate]);

  useEffect(() => {
    setPage(0); // Reset to first page on new search
  }, [searchTerm]);

  useEffect(() => {
    const fetchProblems = async () => {
      try {
        const url = `/problems/?skip=${page * limit}&limit=${limit}${searchTerm ? `&search=${searchTerm}` : ""}`;
        const problemsRes = await API.get(url);
        if (problemsRes.data.length < limit) {
          setHasMore(false);
        } else {
          setHasMore(true);
        }
        setProblems(problemsRes.data);
      } catch (err) {
        console.error("Error fetching problems", err);
      } finally {
        setLoading(false);
      }
    };

    fetchProblems();
  }, [page, searchTerm]);

  const handleSolve = async (problemId) => {
    try {
      await API.post(`/problems/solve/${problemId}`);
      // Refresh stats
      const statsRes = await API.get("/analytics/dashboard");
      setStats(statsRes.data);
      const readinessRes = await API.get("/ml/readiness");
      setReadiness(readinessRes.data.interview_readiness_score);
    } catch (err) {
      console.error("Error marking problem as solved", err);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  const nextPage = () => setPage(prev => prev + 1);
  const prevPage = () => setPage(prev => Math.max(0, prev - 1));

  // Client-side filtering is no longer needed as we filter on the server
  const visibleProblems = useMemo(() => {
    return problems.filter(p => {
      const matchesTopic = filterTopic === "" || p.topic === filterTopic;
      return matchesTopic;
    });
  }, [problems, filterTopic]);

  const topics = useMemo(() => {
    const allTopics = problems.map(p => p.topic);
    return ["", ...new Set(allTopics)];
  }, [problems]);

  if (loading && page === 0) return <div className="loading">Loading Dashboard...</div>;

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <h1>DSA Tracker</h1>
        <div className="header-actions">
          <div className="readiness-chip">
            AI Readiness Score: <strong>{readiness || 0}%</strong>
          </div>
          <button onClick={handleLogout} className="logout-btn">Logout</button>
        </div>
      </header>

      <main className="dashboard-main">
        <section className="stats-section">
          <div className="stat-card readiness-card">
            <h3>Interview Readiness</h3>
            <div className="readiness-gauge">
               <svg viewBox="0 0 36 36" className="circular-chart">
                <path className="circle-bg"
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <path className="circle"
                  strokeDasharray={`${readiness || 0}, 100`}
                  d="M18 2.0845
                    a 15.9155 15.9155 0 0 1 0 31.831
                    a 15.9155 15.9155 0 0 1 0 -31.831"
                />
                <text x="18" y="20.35" className="percentage">{readiness || 0}%</text>
              </svg>
            </div>
          </div>
          <div className="stat-card streak">
            <h3>Current Streak</h3>
            <div className="stat-value">{stats?.current_streak || 0} Days</div>
            <p className="subtext">Longest: {stats?.longest_streak || 0}</p>
          </div>
          <div className="stat-card solved">
            <h3>Total Solved</h3>
            <div className="stat-value">{stats?.total_solved || 0}</div>
          </div>
          <div className="stat-card breakdown">
            <h3>Difficulty Breakdown</h3>
            <div className="difficulty-bars">
              <div className="diff-bar easy">
                <span>Easy: {stats?.easy || 0}</span>
                <div className="progress" style={{ width: `${(stats?.easy / (stats?.total_solved || 1)) * 100}%` }}></div>
              </div>
              <div className="diff-bar medium">
                <span>Medium: {stats?.medium || 0}</span>
                <div className="progress" style={{ width: `${(stats?.medium / (stats?.total_solved || 1)) * 100}%` }}></div>
              </div>
              <div className="diff-bar hard">
                <span>Hard: {stats?.hard || 0}</span>
                <div className="progress" style={{ width: `${(stats?.hard / (stats?.total_solved || 1)) * 100}%` }}></div>
              </div>
            </div>
          </div>
        </section>

        {recommendations.length > 0 && (
          <section className="recommendations-section">
            <h2>AI Recommendations</h2>
            <div className="problems-grid recommendations">
              {recommendations.slice(0, 3).map(p => (
                <div key={`rec-${p.id}`} className="problem-card recommended">
                  <div className="rec-badge">AI Pick</div>
                  <div className="problem-info">
                    <h4>{p.title}</h4>
                    <span className={`difficulty-tag ${p.difficulty.toLowerCase()}`}>{p.difficulty}</span>
                  </div>
                  <p className="topic-tag">{p.topic}</p>
                  <div className="problem-actions">
                    <a href={p.leetcode_link} target="_blank" rel="noopener noreferrer" className="leetcode-link">
                      Solve <i className="external-icon">↗</i>
                    </a>
                    <button onClick={() => handleSolve(p.id)} className="solve-btn">Mark Solved</button>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="problems-section">
          <div className="problems-header">
            <h2>Problem Library</h2>
            <div className="filter-controls">
              <input 
                type="text" 
                placeholder="Search problems..." 
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
              <select 
                value={filterTopic} 
                onChange={(e) => setFilterTopic(e.target.value)}
                className="topic-select"
              >
                <option value="">All Topics</option>
                {topics.filter(t => t !== "").map(t => (
                  <option key={t} value={t}>{t}</option>
                ))}
              </select>
            </div>
            <div className="pagination-controls">
              <button onClick={prevPage} disabled={page === 0} className="page-btn">Previous</button>
              <span>Page {page + 1}</span>
              <button onClick={nextPage} disabled={!hasMore} className="page-btn">Next</button>
            </div>
          </div>
          
          <div className="problems-grid">
            {visibleProblems.length > 0 ? (
              visibleProblems.map(p => (
                <div key={p.id} className="problem-card">
                  <div className="problem-info">
                    <h4>{p.title}</h4>
                    <span className={`difficulty-tag ${p.difficulty.toLowerCase()}`}>{p.difficulty}</span>
                  </div>
                  <p className="topic-tag">{p.topic}</p>
                  <div className="problem-actions">
                    <a href={p.leetcode_link} target="_blank" rel="noopener noreferrer" className="leetcode-link">
                      Solve <i className="external-icon">↗</i>
                    </a>
                    <button onClick={() => handleSolve(p.id)} className="solve-btn">Mark Solved</button>
                  </div>
                </div>
              ))
            ) : (
              <p>No problems found matching your criteria.</p>
            )}
          </div>

          <div className="problems-footer">
            <div className="pagination-controls">
              <button onClick={prevPage} disabled={page === 0} className="page-btn">Previous</button>
              <span>Page {page + 1}</span>
              <button onClick={nextPage} disabled={!hasMore} className="page-btn">Next</button>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default Dashboard;