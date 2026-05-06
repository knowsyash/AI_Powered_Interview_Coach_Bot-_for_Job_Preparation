"use client";

import { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Inter } from "next/font/google";
import { GeistMono } from "geist/font/mono";
import { Globe, Terminal, Coffee, Braces, Database, Users, ChevronRight, TerminalSquare, GitBranch, Code, FileText, Download, X, Minus, Settings, BarChart2, Play, Lightbulb } from "lucide-react";
import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
import Editor from "@monaco-editor/react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip, ResponsiveContainer } from "recharts";



const inter = Inter({ subsets: ["latin"] });

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

type LogEntry = {
  timestamp: string;
  type: "INFO" | "READY" | "WARN" | "SCORE" | "SYSTEM";
  message: string;
};

const categories = [
  { id: "webdev", name: "web-dev", desc: "HTML, CSS, React, Next.js", icon: Globe, difficulty: "intermediate", diffColor: "text-[#F59E0B] bg-[#F59E0B]/10", qCount: 10 },
  { id: "python", name: "python", desc: "Django, Flask, Data Science", icon: Terminal, difficulty: "beginner", diffColor: "text-[#22C55E] bg-[#22C55E]/10", qCount: 10 },
  { id: "java", name: "java", desc: "java", icon: Coffee, difficulty: "advanced", diffColor: "text-[#EF4444] bg-[#EF4444]/10", qCount: 10 },
  { id: "javascript", name: "node-js", desc: "React, Angular, Node", icon: Braces, difficulty: "intermediate", diffColor: "text-[#F59E0B] bg-[#F59E0B]/10", qCount: 10 },
  { id: "database", name: "database", desc: "MySQL, PostgreSQL, MongoDB", icon: Database, difficulty: "intermediate", diffColor: "text-[#F59E0B] bg-[#F59E0B]/10", qCount: 10 },
  { id: "behavioral", name: "behavioral", desc: "STAR Format, Leadership", icon: Users, difficulty: "beginner", diffColor: "text-[#22C55E] bg-[#22C55E]/10", qCount: 10 },
];

export default function Home() {
  const [category, setCategory] = useState<string | null>(null);
  const [question, setQuestion] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string>("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [timer, setTimer] = useState<number>(0);
  const [isTimerRunning, setIsTimerRunning] = useState<boolean>(false);
  const [latestFeedback, setLatestFeedback] = useState<any>(null); // eslint-disable-line @typescript-eslint/no-explicit-any
  const [questionNumber, setQuestionNumber] = useState<number>(1);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [activeTab, setActiveTab] = useState<"question" | "feedback" | "analytics" | "settings" | "report">("question");

  const [isCodeMode, setIsCodeMode] = useState(false);
  
  // Settings State
  const [experienceLevel, setExperienceLevel] = useState<"junior" | "mid" | "senior">("junior");
  const [strictness, setStrictness] = useState<"lenient" | "normal" | "strict">("normal");

  // Session State
  const [sessionMode, setSessionMode] = useState<boolean>(false);
  const [sessionQuestionsCount, setSessionQuestionsCount] = useState<number>(0);
  const [sessionHistory, setSessionHistory] = useState<any[]>([]);
  
  // Hints State
  const [hintUsed, setHintUsed] = useState<boolean>(false);
  const [hintText, setHintText] = useState<string | null>(null);

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const [expandedSections, setExpandedSections] = useState({ strengths: true, improvements: true, model: false });
  const [showLogsPanel, setShowLogsPanel] = useState<boolean>(true);
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const logsEndRef = useRef<HTMLDivElement>(null);

  const addLog = (type: LogEntry["type"], message: string) => {
    const now = new Date();
    const timeString = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
    setLogs(prev => [...prev, { timestamp: timeString, type, message }]);
    setShowLogsPanel(true);
  };

  // Anti-Cheat: Visibility Logging
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden && isTimerRunning) {
        addLog("WARN", "[ANTI-CHEAT] Focus lost - tab switched");
      }
    };
    document.addEventListener("visibilitychange", handleVisibilityChange);
    return () => document.removeEventListener("visibilitychange", handleVisibilityChange);
  }, [isTimerRunning]);

  const [isWakingUp, setIsWakingUp] = useState<boolean>(true);

  useEffect(() => {
    // Only show loader for non-localhost
    if (typeof window !== "undefined") {
      const isLocalhost = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
      if (isLocalhost) {
        setIsWakingUp(false);
        return;
      }
    }

    const checkHealth = async () => {
      try {
        const response = await fetch('/api/health');
        if (response.ok) {
          setIsWakingUp(false);
        } else {
          setTimeout(checkHealth, 2000);
        }
      } catch (error) {
        setTimeout(checkHealth, 2000);
      }
    };
    checkHealth();
  }, []);

  const exportPDF = async () => {
    if (typeof window === "undefined") return;
    addLog("INFO", "Generating PDF report...");
    const html2pdf = (await import("html2pdf.js")).default;
    const element = document.getElementById("feedback-report");
    if (element) {
      html2pdf().from(element).save(`interview_report_${category}_q${questionNumber}.pdf`);
      addLog("READY", "PDF Exported");
    }
  };

  useEffect(() => {
    if (logsEndRef.current && showLogsPanel) logsEndRef.current.scrollIntoView({ behavior: "smooth" });
  }, [logs, showLogsPanel]);


  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isTimerRunning) interval = setInterval(() => setTimer((prev) => prev + 1), 1000);
    return () => clearInterval(interval);
  }, [isTimerRunning]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s < 10 ? "0" : ""}${s}`;
  };

  const getScoreColor = (score: number) => score >= 75 ? "#22C55E" : score >= 50 ? "#F59E0B" : "#EF4444";

  const selectCategory = async (categoryId: string) => {
    const catName = categories.find(c => c.id === categoryId)?.name || categoryId;
    addLog("INFO", `initializing ${catName} environment...`);
    setCategory(categoryId);
    setQuestionNumber(1);
    setLatestFeedback(null);
    setActiveTab("question");
    setTimeout(async () => {
      addLog("READY", `${catName} loaded`);
      await getQuestion(categoryId);
    }, 300);
  };

  const getQuestion = async (categoryOverride?: string) => {
    const activeCategory = categoryOverride || category;
    if (!activeCategory) return;

    addLog("INFO", `requesting question ${questionNumber.toString().padStart(2, '0')}...`);

    try {
      const response = await fetch(`/api/question?category=${activeCategory}`);
      const data = await response.json();
      setQuestion(data.question);
      setSessionId(data.session_id);
      setAnswer("");
      setTimer(0);
      setIsTimerRunning(true);
      setActiveTab("question");
      setLatestFeedback(null);
      addLog("INFO", `question ${questionNumber.toString().padStart(2, '0')} served`);
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-explicit-any
      addLog("WARN", "failed to fetch question");
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.ctrlKey && e.key === 'Enter') submitAnswer();
  };

  const submitAnswer = async () => {
    if (!question || !answer.trim()) return;

    setIsTimerRunning(false);

    const wordCount = answer.trim().split(/\s+/).length;
    addLog("INFO", `response received (${wordCount} words)`);
    addLog("SCORE", "analyzing...");

    try {
      const response = await fetch("/api/answer", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question, answer, category, session_id: sessionId, experienceLevel, strictness, hintUsed, receivedHint: hintText }),
      });
      const data = await response.json();

      if (!response.ok || data?.error) {
        addLog("WARN", data?.error || "analysis failed");
        return;
      }
      
      if (data.is_foul) {
        addLog("WARN", "copied form hint direclty faoul 0 marks etc");
      }

      const newFeedback = { question, answer, ...data };
      setLatestFeedback(newFeedback);

      // Save locally to simulate Analytics
      const localHistory = JSON.parse(localStorage.getItem('interview_history') || '[]');
      localHistory.push({ date: new Date().toLocaleDateString(), score: data.score, category: category || 'unknown' });
      localStorage.setItem('interview_history', JSON.stringify(localHistory));

      addLog("READY", "analysis complete");
      
      if (sessionMode) {
        const newHistory = [...sessionHistory, newFeedback];
        setSessionHistory(newHistory);
        if (questionNumber >= 5) {
          setActiveTab("report");
          setSessionQuestionsCount(5);
        } else {
          setActiveTab("feedback");
        }
      } else {
        setActiveTab("feedback");
      }
    } catch (error: any) { // eslint-disable-line @typescript-eslint/no-unused-vars, @typescript-eslint/no-explicit-any
      addLog("WARN", "analysis failed");
    }
  };

  const skipQuestion = async () => {
    if (!sessionId) return;
    addLog("INFO", "Skipping question...");
    try {
      const response = await fetch("/api/skip", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });
      if (!response.ok) {
        addLog("WARN", "failed to skip question");
        return;
      }
      
      const newFeedback = {
        question: question || "Unknown",
        answer: "[SKIPPED]",
        score: 0,
        feedback: "Question skipped by user."
      };
      
      if (sessionMode) {
        const newHistory = [...sessionHistory, newFeedback];
        setSessionHistory(newHistory);
        if (questionNumber >= 5) {
          setActiveTab("report");
          setSessionQuestionsCount(5);
        } else {
          setQuestionNumber(prev => prev + 1);
          await getQuestion();
        }
      } else {
        setQuestionNumber(prev => prev + 1);
        await getQuestion();
      }
    } catch (error) {
      addLog("WARN", "error skipping question");
    }
  };

  const resetSession = () => {
    addLog("WARN", "session terminated");
    setCategory(null);
    setQuestion(null);
    setAnswer("");
    setSessionId(null);
    setTimer(0);
    setIsTimerRunning(false);
    setLatestFeedback(null);
    setSessionHistory([]);
    setQuestionNumber(1);
    setHintUsed(false);
    setHintText(null);
  };

  const getHint = async () => {
    if (!sessionId) return;
    setHintUsed(true);
    addLog("INFO", "Hint requested. Max score reduced by 10%.");
    setHintText("Loading hint...");
    
    try {
      const response = await fetch("/api/hint", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId }),
      });
      const data = await response.json();
      
      if (!response.ok || data?.error) {
        setHintText("Break the problem into smaller concepts and address them one by one.");
        return;
      }
      
      setHintText(data.hint);
    } catch (error) {
      setHintText("Consider using the STAR format or breaking the problem down into smaller steps.");
    }
  };

  const validateCode = () => {
    try {
      // Basic syntax validation using new Function
      new Function(answer);
      addLog("READY", "Syntax validation passed: No errors found.");
    } catch (err: any) {
      addLog("WARN", `Syntax Error: ${err.message}`);
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  const toggleSection = (section: keyof typeof expandedSections) => {
    setExpandedSections(prev => ({ ...prev, [section]: !prev[section] }));
  };

  const activeCategoryObj = categories.find(c => c.id === category);
  const wordCount = answer.trim() ? answer.trim().split(/\s+/).length : 0;

  if (isWakingUp) {
    return (
      <div className={cn(inter.className, "min-h-screen bg-[#1E1E1E] flex flex-col items-center justify-center p-8")}>
        <div className="flex flex-col items-center max-w-md w-full">
          <TerminalSquare className="w-16 h-16 text-[#007ACC] mb-6 animate-pulse" />
          <h1 className="text-2xl font-light text-[#FFFFFF] mb-2">Initializing Workspace...</h1>
          <p className="text-sm text-[#858585] text-center mb-8">
            The backend service is starting up. This usually takes 30-60 seconds on the free tier.
          </p>
          <div className="w-full bg-[#2D2D30] rounded-full h-1.5 overflow-hidden">
            <motion.div 
              className="bg-[#007ACC] h-full"
              initial={{ width: "0%" }}
              animate={{ width: "100%" }}
              transition={{ duration: 2, repeat: Infinity }}
            />
          </div>
          <p className={cn(GeistMono.className, "text-xs text-[#569CD6] mt-4 animate-pulse")}>
            Polling /api/health...
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className={cn(inter.className, "min-h-screen bg-[#1E1E1E] text-[#CCCCCC] flex flex-col overflow-hidden pb-[24px]")}>

      <header className="h-[35px] shrink-0 bg-[#333333] border-b border-[#252526] flex items-center px-4 z-20 shadow-sm">
        <div className="flex items-center gap-3">
          <TerminalSquare className="w-[14px] h-[14px] text-[#007ACC]" />
          <div className={cn(GeistMono.className, "text-xs flex items-center gap-1.5")}>
            <span className="text-[#CCCCCC]">VS Interviewer</span>
            <span className="text-[#555555]">-</span>
            <span className={category ? "text-[#4EC9B0]" : "text-[#888888]"}>{activeCategoryObj?.name || "No Workspace"}</span>
          </div>
        </div>
      </header>

      <div className="flex-1 flex overflow-hidden">
        <aside className="w-[250px] shrink-0 bg-[#252526] border-r border-[#333333] hidden md:flex flex-col">
          <div className={cn(GeistMono.className, "text-[11px] font-semibold tracking-wider text-[#BBBBBB] uppercase px-4 pt-3 pb-2")}>EXPLORER</div>
          <div className="flex-1 overflow-y-auto">
            <div className="px-4 py-1 text-[#858585] text-[10px] font-bold uppercase tracking-wider">Categories</div>
            {categories.map((cat) => (
              <div key={cat.id} onClick={() => !category && selectCategory(cat.id)} className={cn("h-7 px-4 flex items-center gap-2 cursor-pointer transition-colors duration-100", category === cat.id ? "bg-[#37373D] text-[#FFFFFF]" : "text-[#CCCCCC] hover:bg-[#2A2D2E]", category && category !== cat.id && "opacity-50 cursor-not-allowed hover:bg-transparent")}>
                <ChevronRight className={cn("w-3 h-3 text-[#444444]", category === cat.id && "text-[#CCCCCC] rotate-90")} />
                <cat.icon className="w-[14px] h-[14px] shrink-0" />
                <span className="text-[13px] truncate flex-1">{cat.name}</span>
              </div>
            ))}
            
            <div className="mt-4 px-4 py-1 text-[#858585] text-[10px] font-bold uppercase tracking-wider">Application</div>
            <div onClick={() => { setActiveTab("analytics"); setCategory(null); }} className={cn("h-7 px-4 flex items-center gap-2 cursor-pointer transition-colors duration-100", activeTab === "analytics" ? "bg-[#37373D] text-[#FFFFFF]" : "text-[#CCCCCC] hover:bg-[#2A2D2E]")}>
              <BarChart2 className="w-[14px] h-[14px] shrink-0" />
              <span className="text-[13px] truncate flex-1">analytics.json</span>
            </div>
            <div onClick={() => { setActiveTab("settings"); setCategory(null); }} className={cn("h-7 px-4 flex items-center gap-2 cursor-pointer transition-colors duration-100", activeTab === "settings" ? "bg-[#37373D] text-[#FFFFFF]" : "text-[#CCCCCC] hover:bg-[#2A2D2E]")}>
              <Settings className="w-[14px] h-[14px] shrink-0" />
              <span className="text-[13px] truncate flex-1">settings.json</span>
            </div>
          </div>
        </aside>

        <main className="flex-1 flex flex-col bg-[#1E1E1E] overflow-hidden relative">
          <AnimatePresence mode="wait">
            {!category ? (
              <motion.div key="page1" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex-1 flex flex-col overflow-y-auto w-full max-w-5xl mx-auto p-10">
                <h1 className="text-3xl font-light text-[#FFFFFF] mb-2 tracking-wide">Start session</h1>
                <p className="text-sm text-[#AAAAAA] mb-8">Select a technology stack from the explorer to begin mock interview.</p>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {categories.map((cat) => (
                    <div key={cat.id} onClick={() => selectCategory(cat.id)} className="bg-[#2D2D30] border border-[#3E3E42] p-4 rounded hover:bg-[#3E3E42] cursor-pointer transition">
                      <div className="flex items-center gap-3 mb-2">
                        <cat.icon className="w-6 h-6 text-[#4EC9B0]" />
                        <h3 className="text-[#CCCCCC] font-medium">{cat.name}</h3>
                      </div>
                      <p className={cn(GeistMono.className, "text-[#999999] text-xs")}>{cat.desc}</p>
                    </div>
                  ))}
                </div>
              </motion.div>
            ) : (
              <motion.div key="page2" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex-1 flex flex-col overflow-hidden">
                <div className="h-9 bg-[#2D2D30] flex items-end">
                  {["question", "feedback", "analytics", "settings", "report"].map((tab) => {
                    if ((tab === "feedback" && !latestFeedback) || (tab === "report" && sessionHistory.length === 0)) return null;
                    return (
                      <div key={tab} onClick={() => setActiveTab(tab as any)} className={cn("h-9 px-4 border-r border-[#1E1E1E] flex items-center gap-2 cursor-pointer", activeTab === tab ? "bg-[#1E1E1E] text-[#FFFFFF] border-t border-t-[#007ACC]" : "bg-[#2D2D30] text-[#969696] hover:bg-[#2A2D2E]")}>
                        <span className={cn(GeistMono.className, "text-[13px]")}>{tab}.ts</span>
                      </div>
                    )
                  })}
                </div>

                <div className="flex-1 overflow-y-auto px-8 py-6 max-w-5xl mx-auto w-full">
                  {activeTab === "question" && question ? (
                    <div className="flex flex-col h-full">
                      <div className={cn(GeistMono.className, "text-[12px] text-[#569CD6] mb-6")}>
                        {"// Question "} {questionNumber} {" ΓÇó Timer: "} <span className={isTimerRunning ? "text-[#CE9178]" : "text-[#AAAAAA]"}>{formatTime(timer)}</span>
                      </div>

                      <div className="mb-6 font-medium text-[15px] text-[#D4D4D4] leading-relaxed">
                        {question}
                      </div>

                      <div className="flex items-center gap-3 mb-3 flex-wrap">
                        <button
                          onClick={() => setIsCodeMode(!isCodeMode)}
                          className={cn("flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded shadow-sm border transition-all", isCodeMode ? "bg-[#007ACC] text-white border-[#007ACC]" : "bg-[#333333] text-[#CCCCCC] border-[#444444] hover:bg-[#444444]")}
                        >
                          {isCodeMode ? <Code className="w-3.5 h-3.5" /> : <FileText className="w-3.5 h-3.5" />}
                          {isCodeMode ? "Code Editor Mode" : "Plain Text Mode"}
                        </button>
                        
                        {isCodeMode && (
                          <button onClick={validateCode} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded shadow-sm border transition-all bg-[#333333] text-[#CCCCCC] border-[#444444] hover:bg-[#444444]">
                            <Play className="w-3.5 h-3.5 text-[#4EC9B0]" /> Validate Syntax
                          </button>
                        )}
                        
                        <button onClick={getHint} disabled={hintUsed} className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded shadow-sm border transition-all bg-[#333333] text-[#CCCCCC] border-[#444444] hover:bg-[#444444] disabled:opacity-50">
                          <Lightbulb className={cn("w-3.5 h-3.5", hintUsed ? "text-[#CE9178]" : "text-[#F59E0B]")} /> {hintUsed ? "Hint Used" : "Request Hint (-10% Score)"}
                        </button>
                      </div>
                      
                      {hintText && (
                        <div className="mb-4 p-3 bg-[#CE9178]/10 border border-[#CE9178]/30 rounded text-[#CE9178] text-sm flex items-start gap-2">
                          <Lightbulb className="w-4 h-4 mt-0.5 shrink-0" />
                          <div>
                            <strong>Hint:</strong> {hintText}
                          </div>
                        </div>
                      )}

                      <div className="flex-1 min-h-[350px] border border-[#3C3C3C] bg-[#1E1E1E] rounded-sm flex flex-col relative focus-within:border-[#007ACC] transition-colors">
                        {isCodeMode ? (
                          <Editor
                            height="100%"
                            defaultLanguage="javascript"
                            theme="vs-dark"
                            value={answer}
                            onChange={(val) => setAnswer(val || "")}
                            options={{ minimap: { enabled: false }, padding: { top: 16 }, fontSize: 13, fontFamily: "Geist Mono, monospace" }}
                          />
                        ) : (
                          <textarea
                            value={answer}
                            onChange={(e) => setAnswer(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Type your response here..."
                            className={cn(GeistMono.className, "flex-1 w-full bg-transparent p-4 text-[14px] text-[#D4D4D4] leading-relaxed focus:outline-none resize-none")}
                          />
                        )}
                        <div className="border-t border-[#3C3C3C] px-3 py-1.5 bg-[#252526] flex justify-between items-center text-[#858585] text-[11px] rounded-b-sm">
                          <span>Ln 1, Col 1</span>
                          <div className="flex gap-4">
                            <span>{wordCount} words</span>
                            <span>UTF-8</span>
                            <span>CRLF</span>
                            <span className={isCodeMode ? "text-[#4EC9B0]" : "text-[#CE9178]"}>{isCodeMode ? "JavaScript" : "Plain Text"}</span>
                          </div>
                        </div>
                      </div>

                      <div className="mt-6 flex justify-between items-center">
                        <button onClick={resetSession} className="text-xs text-[#858585] hover:text-[#CE9178]">Γûá Stop Session</button>
                        <div className="flex gap-3">
                          <button onClick={skipQuestion} className="bg-[#333333] hover:bg-[#444444] border border-[#444444] text-[#CCCCCC] px-5 py-2 text-sm font-medium rounded shadow-sm transition-colors">
                            Skip Question
                          </button>
                          <button onClick={submitAnswer} disabled={!answer.trim() || !isTimerRunning} className="bg-[#0E639C] hover:bg-[#1177BB] text-white px-5 py-2 text-sm font-medium rounded shadow-sm disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2">
                            Submit Response (Ctrl+Enter)
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : null}

                  {activeTab === "feedback" && latestFeedback ? (
                    <div className="flex flex-col h-full" id="feedback-report">
                      <div className="flex justify-between items-center mb-6">
                        <h2 className="text-xl font-light text-white">Evaluation Results</h2>
                        <div className="flex gap-3">
                          <button onClick={exportPDF} className="flex items-center gap-2 px-3 py-1.5 text-xs bg-[#333333] border border-[#444444] rounded hover:bg-[#444444] text-[#CCCCCC]"><Download className="w-3.5 h-3.5" /> Export Config & Results</button>
                          <div className="px-3 py-1.5 text-sm font-bold bg-[#252526] border border-[#333333] rounded" style={{ color: getScoreColor(latestFeedback.score * 10 || 0) }}>
                            Score: {latestFeedback.score || 0}/10
                          </div>
                        </div>
                      </div>

                      <div className="mb-6 bg-[#252526] border border-[#3C3C3C] p-4 rounded text-sm text-[#D4D4D4] leading-relaxed">
                        <span className="text-[#569CD6] font-mono block mb-1">{"// Question"}</span>
                        {latestFeedback.question}
                      </div>

                      <div className="space-y-3 mb-6">
                        <div className="bg-[#1E1E1E] border border-[#3C3C3C] rounded">
                          <div className="bg-[#2D2D30] px-4 py-2 text-sm text-[#CCCCCC] font-medium border-b border-[#3C3C3C]">Analysis & Feedback</div>
                          <div className="p-4 text-sm text-[#D4D4D4] leading-relaxed"><span className="text-[#4EC9B0]">Γ£ô</span> {latestFeedback.feedback}</div>
                        </div>
                        
                        {latestFeedback.reference_answer && (
                          <div className="bg-[#1E1E1E] border border-[#3C3C3C] rounded mt-4">
                            <div className="bg-[#2D2D30] px-4 py-2 text-sm text-[#CCCCCC] font-medium border-b border-[#3C3C3C]">Reference Answer Example</div>
                            <div className="p-4 text-sm text-[#858585] italic leading-relaxed">
                              {latestFeedback.reference_answer}
                            </div>
                          </div>
                        )}
                      </div>

                      <div className="flex justify-end mt-4">
                        <button onClick={() => {
                          setHintUsed(false);
                          setHintText(null);
                          if (!sessionMode || questionNumber < 5) {
                              setQuestionNumber(prev => prev + 1);
                          }
                          getQuestion();
                        }} className="bg-[#0E639C] hover:bg-[#1177BB] text-white px-5 py-2 text-sm font-medium rounded shadow-sm">
                          {sessionMode && questionNumber >= 5 ? "Finish Session" : "Next Question ΓåÆ"}
                        </button>
                      </div>
                    </div>
                  ) : null}

                  {activeTab === "settings" ? (
                    <div className="flex flex-col h-full animate-in fade-in max-w-2xl">
                      <h2 className="text-xl font-light text-white mb-6">Settings & Configuration</h2>
                      <div className="space-y-6">
                        <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded">
                          <h3 className="text-sm font-medium text-[#D4D4D4] mb-4">Experience Level</h3>
                          <div className="flex gap-4">
                            {["junior", "mid", "senior"].map(level => (
                              <button key={level} onClick={() => setExperienceLevel(level as any)} className={cn("px-4 py-2 rounded text-sm capitalize border transition", experienceLevel === level ? "bg-[#0E639C] border-[#0E639C] text-white" : "bg-[#1E1E1E] border-[#3C3C3C] text-[#CCCCCC] hover:bg-[#2A2D2E]")}>{level}</button>
                            ))}
                          </div>
                          <p className="text-[#858585] text-xs mt-3">Adjusts the expected complexity and serves appropriate questions.</p>
                        </div>
                        <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded">
                          <h3 className="text-sm font-medium text-[#D4D4D4] mb-4">Evaluation Strictness</h3>
                          <div className="flex gap-4">
                            {["lenient", "normal", "strict"].map(level => (
                              <button key={level} onClick={() => setStrictness(level as any)} className={cn("px-4 py-2 rounded text-sm capitalize border transition", strictness === level ? "bg-[#0E639C] border-[#0E639C] text-white" : "bg-[#1E1E1E] border-[#3C3C3C] text-[#CCCCCC] hover:bg-[#2A2D2E]")}>{level}</button>
                            ))}
                          </div>
                          <p className="text-[#858585] text-xs mt-3">Determines how harshly the AI evaluator grades your answers.</p>
                        </div>
                        <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded">
                          <h3 className="text-sm font-medium text-[#D4D4D4] mb-4">Session Mode</h3>
                          <div className="flex gap-4 items-center">
                            <button onClick={() => setSessionMode(!sessionMode)} className={cn("px-4 py-2 rounded text-sm border transition", sessionMode ? "bg-[#22C55E]/20 border-[#22C55E]/50 text-[#22C55E]" : "bg-[#1E1E1E] border-[#3C3C3C] text-[#CCCCCC] hover:bg-[#2A2D2E]")}>
                              {sessionMode ? "Enabled (5 Questions)" : "Disabled (Continuous)"}
                            </button>
                          </div>
                          <p className="text-[#858585] text-xs mt-3">Group interviews into 5-question mock sessions with a final report card.</p>
                        </div>
                      </div>
                    </div>
                  ) : null}

                  {activeTab === "analytics" ? (
                    <div className="flex flex-col h-full animate-in fade-in">
                      <h2 className="text-xl font-light text-white mb-6">Performance Analytics</h2>
                      <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded w-full h-[400px]">
                        <h3 className="text-sm font-medium text-[#D4D4D4] mb-6">Recent Scores History</h3>
                        {(() => {
                          let history = [];
                          if (typeof window !== "undefined") {
                            history = JSON.parse(localStorage.getItem('interview_history') || '[]');
                          }
                          if (history.length === 0) return <div className="text-[#858585] text-sm">No interview data available yet. Complete a session first.</div>;
                          return (
                            <ResponsiveContainer width="100%" height="100%">
                              <LineChart data={history.slice(-15)}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#3C3C3C" />
                                <XAxis dataKey="date" stroke="#858585" fontSize={12} tickFormatter={(val) => val.substring(0, 5)} />
                                <YAxis stroke="#858585" fontSize={12} domain={[0, 100]} />
                                <RechartsTooltip contentStyle={{ backgroundColor: '#1E1E1E', borderColor: '#3C3C3C', color: '#CCCCCC' }} />
                                <Line type="monotone" dataKey="score" stroke="#4EC9B0" strokeWidth={2} dot={{ fill: '#4EC9B0', strokeWidth: 2 }} />
                              </LineChart>
                            </ResponsiveContainer>
                          );
                        })()}
                      </div>
                    </div>
                  ) : null}

                  {activeTab === "report" && sessionHistory.length > 0 ? (
                    <div className="flex flex-col h-full animate-in fade-in max-w-3xl mx-auto" id="feedback-report">
                      <h2 className="text-2xl font-light text-white mb-2">Mock Interview Session Report</h2>
                      <p className="text-[#858585] mb-8">Completed 5 questions in {category} ΓÇó Level: {experienceLevel}</p>
                      
                      <div className="grid grid-cols-2 gap-4 mb-8">
                        <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded text-center">
                          <div className="text-[#858585] text-sm mb-2">Average Score</div>
                          <div className="text-4xl font-bold" style={{ color: getScoreColor(sessionHistory.reduce((a, b) => a + (b.score || 0), 0) / sessionHistory.length) }}>
                            {Math.round(sessionHistory.reduce((a, b) => a + (b.score || 0), 0) / sessionHistory.length)}/100
                          </div>
                        </div>
                        <div className="bg-[#252526] border border-[#3C3C3C] p-6 rounded text-center">
                          <div className="text-[#858585] text-sm mb-2">Verdict</div>
                          <div className={cn("text-2xl font-semibold mt-3", sessionHistory.reduce((a, b) => a + (b.score || 0), 0) / sessionHistory.length > 70 ? "text-[#4EC9B0]" : "text-[#CE9178]")}>
                            {sessionHistory.reduce((a, b) => a + (b.score || 0), 0) / sessionHistory.length > 70 ? "Pass (Strong)" : "Needs Review"}
                          </div>
                        </div>
                      </div>

                      <h3 className="text-lg font-light text-white mb-4 border-b border-[#3C3C3C] pb-2">Detailed Breakdown</h3>
                      <div className="space-y-4 mb-8">
                        {sessionHistory.map((h, i) => (
                          <div key={i} className="bg-[#1E1E1E] border border-[#3C3C3C] rounded p-4">
                            <div className="flex justify-between items-start mb-2">
                              <h4 className="text-[#D4D4D4] font-medium text-sm w-3/4">Q{i + 1}: {h.question}</h4>
                              <span className="font-bold text-sm" style={{ color: getScoreColor(h.score || 0) }}>{h.score || 0}/100</span>
                            </div>
                            <p className="text-[#858585] text-xs line-clamp-2 mt-2 bg-[#252526] p-2 rounded">{h.feedback}</p>
                          </div>
                        ))}
                      </div>

                      <div className="flex justify-center mt-4 mb-8">
                        <button onClick={resetSession} className="bg-[#0E639C] hover:bg-[#1177BB] text-white px-8 py-3 text-sm font-medium rounded shadow-sm">
                          Start New Session
                        </button>
                      </div>
                    </div>
                  ) : null}
                </div>

                {/* VS Code Style Docked Output Terminal */}
                {showLogsPanel && logs.length > 0 && (
                  <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: "200px", opacity: 1 }} className="border-t border-[#3C3C3C] bg-[#1E1E1E] flex flex-col z-40 shrink-0 w-full">
                    <div className="h-9 flex items-center justify-between px-4 border-b border-[#3C3C3C]">
                      <div className="flex items-center gap-6 h-full">
                        <span className="text-[11px] tracking-wide text-[#858585] cursor-pointer hover:text-[#CCCCCC]">PROBLEMS</span>
                        <span className="text-[11px] font-medium tracking-wide text-[#E7E7E7] border-b border-[#007ACC] h-full flex items-center">OUTPUT</span>
                        <span className="text-[11px] tracking-wide text-[#858585] cursor-pointer hover:text-[#CCCCCC]">DEBUG CONSOLE</span>
                        <span className="text-[11px] tracking-wide text-[#858585] cursor-pointer hover:text-[#CCCCCC]">TERMINAL</span>
                      </div>
                      <div className="flex gap-2">
                        <button onClick={() => setShowLogsPanel(false)} className="text-[#858585] hover:text-[#FFFFFF]"><Minus className="w-4 h-4" /></button>
                        <button onClick={() => setLogs([])} className="text-[#858585] hover:text-[#FFFFFF]"><X className="w-4 h-4" /></button>
                      </div>
                    </div>
                    <div className="flex-1 overflow-y-auto p-4 text-[13px] font-mono leading-relaxed bg-[#1E1E1E]">
                      {logs.map((log, i) => (
                        <div key={i} className="mb-1 whitespace-pre-wrap">
                          <span className="text-[#858585] mr-3">[{log.timestamp}]</span>
                          <span className={cn(log.type === "INFO" ? "text-[#569CD6]" : log.type === "READY" ? "text-[#4EC9B0]" : log.type === "WARN" ? "text-[#CE9178]" : "text-[#CCCCCC]")}>{log.message}</span>
                        </div>
                      ))}
                      <div ref={logsEndRef} />
                    </div>
                  </motion.div>
                )}

              </motion.div>
            )}
          </AnimatePresence>
        </main>
      </div>

      {/* VS CODE STATUS BAR */}
      <footer className="h-[22px] shrink-0 bg-[#007ACC] fixed bottom-0 w-full z-50 flex justify-between items-center px-3 text-white text-[11px] font-medium">
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-1.5 hover:bg-[#ffffff20] px-2 py-0.5 cursor-pointer rounded-sm"><GitBranch className="w-3.5 h-3.5" /><span>main*</span></div>
          <div className="flex items-center gap-1.5 hover:bg-[#ffffff20] px-2 py-0.5 cursor-pointer rounded-sm"><X className="w-3.5 h-3.5" /> 0 ΓÜá 0</div>
          <span>interview-coach Workspace</span>
        </div>
        <div className="flex items-center gap-4">
          <span>Prettier: Γ£ô</span>
          <span>UTF-8</span>
          <span>React</span>
        </div>
      </footer>
    </div>
  );
}
