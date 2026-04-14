import { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { 
  Search, BookOpen, Layers, Edit3, CheckCircle, BrainCircuit, Loader2, Play 
} from 'lucide-react';
import './App.css';

function App() {
  const [topic, setTopic] = useState('');
  const [isResearching, setIsResearching] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [report, setReport] = useState(null);
  
  const steps = [
    { id: 1, title: 'Web Search', desc: 'Scouting for the latest sources.', icon: Search },
    { id: 2, title: 'Deep Reading', desc: 'Scraping and analyzing content.', icon: BookOpen },
    { id: 3, title: 'Drafting Report', desc: 'Synthesizing the gathered data.', icon: Edit3 },
    { id: 4, title: 'Peer Review', desc: 'Evaluating draft for quality.', icon: Layers },
    { id: 5, title: 'Publishing', desc: 'Finalizing polished research.', icon: CheckCircle }
  ];

  const handleResearch = async () => {
    if (!topic.trim()) return;
    
    setIsResearching(true);
    setReport(null);
    setCurrentStep(1);

    // Simulate progress steps if we don't have websocket
    const progressInterval = setInterval(() => {
      setCurrentStep(prev => prev < 4 ? prev + 1 : prev);
    }, 6000); // Progress a step every 6 seconds artificially while waiting

    try {
      const response = await fetch('http://localhost:8000/api/research', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ topic })
      });
      
      const data = await response.json();
      if(data.final_report) {
        setReport(data.final_report);
        setCurrentStep(5);
      } else {
        setReport('Error: Could not generate report.');
      }
    } catch (error) {
      console.error(error);
      setReport('Failed to connect to the backend server. Is Python FastAPI running?');
    } finally {
      clearInterval(progressInterval);
      setIsResearching(false);
      setCurrentStep(5);
    }
  };

  return (
    <div className="app-container">
      <header>
        <h1>Neural Research OS</h1>
        <p className="subtitle">Automated Multi-Agent Research System</p>
      </header>

      <div className="search-section">
        <input 
          type="text" 
          className="search-input"
          placeholder="Enter a topic to research (e.g. quantum computing breakthrough)"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && !isResearching && handleResearch()}
          disabled={isResearching}
        />
        <button 
          className="search-btn" 
          onClick={handleResearch}
          disabled={!topic.trim() || isResearching}
        >
          {isResearching ? <Loader2 className="spinner" size={20} /> : <Play size={20} />}
          {isResearching ? 'Processing...' : 'Run Pipeline'}
        </button>
      </div>

      <main className="main-content">
        {/* Sidebar Progress */}
        <aside className="glass-panel progress-container">
          <h2><BrainCircuit size={24} /> Engine Status</h2>
          
          <div className="steps-list">
            {steps.map((step, index) => {
              const Icon = step.icon;
              const isActive = isResearching && currentStep === step.id;
              const isCompleted = currentStep > step.id || (report && currentStep === 5);
              
              return (
                <div key={step.id} className={`step-item ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                  <div className={`step-icon ${isActive ? 'active' : ''} ${isCompleted ? 'completed' : ''}`}>
                    {isActive ? <Loader2 className="spinner" size={16} /> : <Icon size={16} />}
                  </div>
                  <div className="step-content">
                    <h3>{step.title}</h3>
                    <p>{step.desc}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </aside>

        {/* Report View */}
        <section className="glass-panel report-view">
          {!report && !isResearching && (
            <div className="empty-state">
              <Layers size={64} />
              <p>Enter a topic above to dispatch the AI agent pipeline.<br/>It will automatically search, read, write, critique, and finalize a report.</p>
            </div>
          )}

          {isResearching && !report && (
            <div className="empty-state">
              <BrainCircuit className="spinner" size={64} />
              <h3>Agents are working...</h3>
              <p>This may take up to a minute depending on the complexity of the topic.</p>
            </div>
          )}

          {report && (
            <>
              <div className="report-header">
                <h2>Generated Report</h2>
                <span className="badge">Topic: {topic}</span>
              </div>
              <div className="report-content">
                <ReactMarkdown>{report}</ReactMarkdown>
              </div>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default App;
