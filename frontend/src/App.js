import React, { useState } from "react";
import axios from "axios";

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [elapsedTime, setElapsedTime] = useState("");
  const [lawCategory, setLawCategory] = useState(""); // 법률 카테고리 추가
  const [chatHistory, setChatHistory] = useState([]); // 대화 기록 추가

  const handleSubmit = async (e) => {
    e.preventDefault();
    setAnswer("답변 생성 중...");
    setElapsedTime("");
    setLawCategory("");

    try {
      const response = await axios.post("http://127.0.0.1:8000/query", { question });
      setAnswer(response.data.answer);
      setElapsedTime(response.data.elapsed_time);
      setLawCategory(response.data.law_category); // 법률 카테고리 업데이트

      // 새로운 질문 & 답변을 대화 기록에 추가
      setChatHistory([...chatHistory, { question, answer: response.data.answer, lawCategory: response.data.law_category }]);

    } catch (error) {
      setAnswer("오류 발생! 다시 시도해 주세요.");
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", textAlign: "center" }}>
      <h1>이한죽하 변호사 AI</h1>
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
      <h3>응답 시간: {elapsedTime}</h3>
      <h3>법률 카테고리: {lawCategory}</h3> {/* 적용된 법률 카테고리 표시 */}

      <h2>대화 기록:</h2>
      <ul>
        {chatHistory.map((chat, index) => (
          <li key={index}>
            <strong>Q:</strong> {chat.question} <br />
            <strong>A:</strong> {chat.answer} <br />
            **법률 카테고리:** {chat.lawCategory} {/* 기록에 법률 카테고리 추가 */}
          </li>
        ))}
      </ul>
    </div>
  );
} export default App;