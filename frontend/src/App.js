import React, { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [elapsedTime, setElapsedTime] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAnswer("답변 생성 중...");

    try {
      const response = await axios.post("http://127.0.0.1:8000/query", {
        question: question,
      });
      setAnswer(response.data.answer);
      setElapsedTime(response.data.elapsed_time);
    } catch (error) {
      setAnswer("오류 발생! 다시 시도해 주세요.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", textAlign: "center" }}>
      <h1>변호사 AI</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="법률 질문을 입력하세요..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          style={{ width: "100%", padding: "10px", marginBottom: "10px" }}
        />
        <button type="submit">질문하기</button>
      </form>
      <h2>AI의 답변:</h2>
      <p>{answer}</p>
      {elapsedTime && <h3>응답 시간: {elapsedTime}</h3>} {/* 응답 시간이 있을 때만 출력 */}
    </div>
  );
}export default App;