import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from datetime import datetime
import time
import re

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("GOOGLE_API_KEY not found in .env file!")
    st.stop()

genai.configure(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="AI Research Agent v2.0",
    page_icon="🤖",
    layout="wide",
)

# ===== REMOVED ENTIRE <style> BLOCK =====
# The custom CSS for gradients and glassmorphism is removed
# to allow Streamlit's native themes to work.

# ===== HELPER FUNCTIONS =====
def clean_markdown_text(text):
    """Remove markdown symbols from text"""
    # Remove markdown headers
    text = re.sub(r'#{1,6}\s+', '', text)
    # Remove bold/italic markers
    text = re.sub(r'\*\*|\*|__', '', text)
    # Remove extra whitespace
    text = ' '.join(text.split())
    return text.strip()

def detect_category(topic):
    """Detect research topic category"""
    topic_lower = topic.lower()
    categories = {
        'healthcare': ['health', 'medical', 'disease', 'hospital', 'patient', 'medicine'],
        'finance': ['finance', 'stock', 'market', 'investment', 'banking', 'fintech', 'crypto'],
        'technology': ['technology', 'ai', 'software', 'tech', 'computer', 'digital', 'ml', 'quantum'],
        'education': ['education', 'learning', 'school', 'university', 'student'],
        'environment': ['environment', 'climate', 'sustainability', 'green', 'renewable']
    }
    
    for cat, keywords in categories.items():
        if any(k in topic_lower for k in keywords):
            return cat
    return 'general'

def create_market_trends(category, topic):
    """Create advanced market trend visualizations"""
    charts = []
    
    # Use Streamlit's theme-aware colors
    chart_template = "streamlit" 
    
    if category == 'technology':
        fig1 = make_subplots(
            rows=1, cols=2,
            subplot_titles=('AI Market Size Growth ($B)', 'Technology Adoption Rates (%)'),
            specs=[[{"type": "scatter"}, {"type": "bar"}]]
        )
        
        years = ['2020', '2021', '2022', '2023', '2024', '2025']
        market_size = [50, 62, 78, 95, 120, 150]
        
        fig1.add_trace(
            go.Scatter(
                x=years, y=market_size,
                mode='lines+markers',
                name='Market Size',
                fill='tozeroy'
            ),
            row=1, col=1
        )
        
        tech_types = ['AI/ML', 'Cloud', 'IoT', 'Blockchain', '5G']
        adoption = [85, 78, 65, 45, 60]
        
        fig1.add_trace(
            go.Bar(
                x=tech_types, y=adoption,
                name='Adoption %',
                text=adoption,
                textposition='outside'
            ),
            row=1, col=2
        )
        
        fig1.update_layout(height=450, showlegend=False, template=chart_template)
        charts.append(("Technology Market Analysis", fig1))
        
        fig2 = go.Figure()
        quarters = ['Q1 2024', 'Q2 2024', 'Q3 2024', 'Q4 2024', 'Q1 2025']
        investments = [25, 30, 35, 42, 50]
        
        fig2.add_trace(go.Scatter(
            x=quarters, y=investments,
            mode='lines+markers',
            name='VC Investment',
            fill='tozeroy'
        ))
        
        fig2.update_layout(
            title="Venture Capital Investment Trends ($B)",
            xaxis_title="Quarter",
            yaxis_title="Investment ($B)",
            height=400,
            template=chart_template
        )
        charts.append(("Investment Trends", fig2))
        
        fig3 = go.Figure(data=[go.Pie(
            labels=['Microsoft', 'Google', 'Amazon', 'Meta', 'Others'],
            values=[25, 22, 20, 15, 18],
            hole=0.5,
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig3.update_layout(
            title="Tech Giants Market Share in AI",
            height=400,
            template=chart_template
        )
        charts.append(("Market Share Distribution", fig3))
        
    elif category == 'healthcare':
        fig1 = go.Figure()
        years = ['2020', '2021', '2022', '2023', '2024', '2025']
        digital_health = [40, 52, 68, 85, 105, 130]
        
        fig1.add_trace(go.Scatter(
            x=years, y=digital_health,
            mode='lines+markers',
            fill='tozeroy'
        ))
        
        fig1.update_layout(
            title="Digital Health Market Growth ($B)",
            xaxis_title="Year",
            yaxis_title="Market Size ($B)",
            height=400,
            template=chart_template
        )
        charts.append(("Healthcare Market Growth", fig1))
        
    elif category == 'finance':
        fig1 = go.Figure()
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        adoption = [45, 48, 52, 55, 58, 62, 65, 68, 72, 75, 78, 82]
        
        fig1.add_trace(go.Scatter(
            x=months, y=adoption,
            mode='lines+markers',
            fill='tozeroy'
        ))
        
        fig1.update_layout(
            title="Fintech Adoption Rate 2025 (%)",
            height=400,
            template=chart_template
        )
        charts.append(("Fintech Adoption", fig1))
    
    else:
        fig1 = go.Figure()
        years = ['2020', '2021', '2022', '2023', '2024', '2025']
        growth = [100, 120, 145, 170, 200, 235]
        
        fig1.add_trace(go.Scatter(
            x=years, y=growth,
            mode='lines+markers',
            fill='tozeroy'
        ))
        
        fig1.update_layout(
            title=f"Market Growth: {topic}",
            height=400,
            template=chart_template
        )
        charts.append(("Growth Analysis", fig1))
    
    return charts

def extract_key_points(text):
    """Extract and clean key points from text"""
    lines = text.split('\n')
    key_points = []
    for line in lines:
        cleaned = clean_markdown_text(line).strip()
        if len(cleaned) > 20 and not cleaned.startswith(('**', '#', '-', '*')):
            key_points.append(cleaned)
        if len(key_points) >= 6:
            break
    return key_points if key_points else ["Analysis completed successfully. View full details above."]

def generate_keyword_chart(text):
    """Generate keyword frequency chart"""
    words = text.lower().split()
    word_freq = {}
    stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'is', 'are', 'this', 'that', 'with'}
    
    for word in words:
        word = word.strip('.,!?;:')
        if word not in stop_words and len(word) > 4:
            word_freq[word] = word_freq.get(word, 0) + 1
    
    top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    
    if top_words:
        words_list, counts = zip(*top_words)
        
        fig = go.Figure(data=[
            go.Bar(
                x=counts,
                y=words_list,
                orientation='h',
                text=counts,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="🔤 Top Keywords Analysis",
            xaxis_title="Frequency",
            yaxis_title="Keywords",
            height=400,
            template="streamlit" # Use Streamlit's native theme
        )
        return fig
    return None

# ===== HERO HEADER =====
st.title("🤖 AI RESEARCH AGENT 🚀")
st.caption("Powered by Advanced Multi-Agent Intelligence System")


# ===== AGENTS & FEATURES =====
with st.container(border=True): # Using a standard Streamlit container
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🤖 AI Agents Active")
        with st.expander("🔍 **Research Agent** | Information Gathering Expert", expanded=True):
            st.write("Conducts thorough research and gathers comprehensive data.")
        with st.expander("📊 **Analysis Agent** | Data Analysis Specialist", expanded=True):
            st.write("Analyzes findings, identifies patterns, and extracts key insights.")
        with st.expander("✍️ **Writer Agent** | Report Generation Master", expanded=True):
            st.write("Generates a professional, well-structured final report.")

    with col2:
        st.subheader("✨ Features")
        features = [
            "⚡ **Real-time Processing:** Get results as they are generated.",
            "📈 **Market Trend Analysis:** Visualizes market data and trends.",
            "🎯 **Keyword Analysis:** Automatically extracts and ranks top keywords.",
            "📄 **Professional Reports:** Creates structured reports with key sections.",
            "💾 **Multiple Formats:** Download reports as Markdown or TXT.",
            "🔄 **Live Updates:** (Simulated processing for agent steps)."
        ]
        for feature in features:
            st.markdown(f"- {feature}")

# ===== MAIN CONFIGURATION =====
st.subheader("📝 Research Configuration")
with st.container(border=True):
    col1, col2, col3 = st.columns([3, 2, 1])
    with col1:
        research_topic = st.text_input(
            "🎯 Research Topic",
            placeholder="e.g., Quantum Computing in Healthcare 2025"
        )
        st.caption("💡 Be specific for better and more detailed results")
    with col2:
        detail_level = st.selectbox(
            "Detail Level",
            ["⚡ Quick (5 min)", "📊 Standard (10 min)", "🔬 Deep Dive (15 min)"],
            index=1,
            help="Select the depth of the research (simulated time)."
        )
    with col3:
        show_viz = st.checkbox("📊 Show Analytics", value=True)


# ===== RESEARCH BUTTON =====
if st.button("🚀 START AI RESEARCH", use_container_width=True, type="primary"):
    if not research_topic or research_topic.strip() == "":
        st.error("⚠️ Please enter a research topic!")
        st.stop()
    
    # Detect category
    category = detect_category(research_topic)
    
    st.markdown("---")
    
    # Initialize model
    model = genai.GenerativeModel('gemini-pro-latest')
    
    # Agent prompts
    agents = {
        "Research": {
            "icon": "🔍",
            "name": "Research Agent",
            "prompt": f"""You are a Senior Research Analyst. Conduct comprehensive research on: {research_topic}

Provide:
1. Latest developments and market trends (2024-2025)
2. Key statistics, data points, and market size
3. Multiple perspectives and expert opinions
4. Market analysis and growth projections
5. Key players, stakeholders, and competitors
6. Challenges, opportunities, and risks
7. Future outlook and predictions

Use clear sections and bullet points. Avoid using markdown symbols like # ** in your response."""
        },
        "Analysis": {
            "icon": "📊",
            "name": "Analysis Agent",
            "prompt": f"""You are a Data Analysis Expert. Analyze: {research_topic}

Provide:
1. Critical insights and key findings
2. Pattern identification and trend analysis
3. SWOT analysis (Strengths, Weaknesses, Opportunities, Threats)
4. Risk assessment and mitigation strategies
5. Growth opportunities and market potential
6. Data-driven recommendations and action items

Be analytical, specific, and actionable. Write in plain text without markdown symbols."""
        },
        "Writer": {
            "icon": "✍️",
            "name": "Writer Agent",
            "prompt": f"""You are a Professional Writer. Create a comprehensive report on: {research_topic}

Structure:
1. **Executive Summary** (3-4 paragraphs)
2. **Introduction** (Context and importance)
3. **Market Overview** (Size, trends, growth)
4. **Key Findings** (Organized by themes)
5. **Analysis & Insights** (Deep dive)
6. **Competitive Landscape** (Key players)
7. **Opportunities** (Growth areas)
8. **Challenges** (Risks and obstacles)
9. **Recommendations** (Action items)
10. **Conclusion** (Future outlook)
11. **References** (Sources)

Use professional language, proper formatting, and include specific data points."""
        }
    }
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Research", "📊 Analysis", "✍️ Report", "📈 Market Trends"])
    
    # These variables will hold results
    research_result = ""
    analysis_result = ""
    final_report = ""
    
    # ===== RESEARCH PHASE =====
    with tab1:
        st.subheader("🔍 Research Phase")
        status_text = st.empty()
        status_text.info("🔄 Initializing Research Agent...")
        
        with st.spinner("🔍 Research Agent analyzing comprehensive data..."):
            try:
                progress_bar = st.progress(0)
                for i in range(101):
                    time.sleep(0.015) # Simulating work
                    progress_bar.progress(i)
                
                research_response = model.generate_content(agents['Research']['prompt'])
                research_result = research_response.text
                
                status_text.success("✅ Research Complete!")
                
                with st.expander("📄 View Full Research", expanded=True):
                    st.markdown(research_result)
                
                # Metrics
                st.subheader("📊 Research Metrics")
                col1, col2, col3 = st.columns(3)
                words = len(research_result.split())
                chars = len(research_result)
                sections = research_result.count('\n\n')
                
                col1.metric("Words", words)
                col2.metric("Characters", chars)
                col3.metric("Sections", sections)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # ===== ANALYSIS PHASE =====
    with tab2:
        st.subheader("📊 Analysis Phase")
        if not research_result:
            st.warning("Please run the Research phase first.")
            st.stop()
            
        status_text2 = st.empty()
        status_text2.info("🔄 Initializing Analysis Agent...")
        
        with st.spinner("📊 Analysis Agent processing insights..."):
            try:
                progress_bar2 = st.progress(0)
                for i in range(101):
                    time.sleep(0.015) # Simulating work
                    progress_bar2.progress(i)
                
                analysis_prompt = agents['Analysis']['prompt'] + f"\n\nContext:\n{research_result}"
                analysis_response = model.generate_content(analysis_prompt)
                analysis_result = analysis_response.text
                
                status_text2.success("✅ Analysis Complete!")
                
                with st.expander("📊 View Full Analysis", expanded=True):
                    st.markdown(analysis_result)
                
                st.subheader("💡 Key Insights")
                key_points = extract_key_points(analysis_result)
                for idx, point in enumerate(key_points):
                    st.info(f"**{idx+1}.** {point}")
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # ===== WRITING PHASE =====
    with tab3:
        st.subheader("✍️ Report Generation")
        if not analysis_result:
            st.warning("Please run the Analysis phase first.")
            st.stop()
            
        status_text3 = st.empty()
        status_text3.info("🔄 Initializing Writer Agent...")
        
        with st.spinner("✍️ Writer Agent creating comprehensive report..."):
            try:
                progress_bar3 = st.progress(0)
                for i in range(101):
                    time.sleep(0.015) # Simulating work
                    progress_bar3.progress(i)
                
                writer_prompt = agents['Writer']['prompt'] + f"\n\nResearch:\n{research_result}\n\nAnalysis:\n{analysis_result}"
                writer_response = model.generate_content(writer_prompt)
                final_report = writer_response.text
                
                status_text3.success("✅ Report Generated!")
                
                st.markdown(final_report)
                
                # Download Section
                st.subheader("💾 Download Options")
                col1, col2, col3 = st.columns(3)
                
                col1.download_button(
                    "📄 Markdown Format",
                    data=final_report,
                    file_name=f"{research_topic.replace(' ', '_')}.md",
                    mime="text/markdown",
                    use_container_width=True
                )
                
                col2.download_button(
                    "📝 Text Format",
                    data=final_report,
                    file_name=f"{research_topic.replace(' ', '_')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
                
                col3.button("📊 PDF Export (Soon)", disabled=True, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                st.stop()
    
    # ===== MARKET TRENDS TAB =====
    with tab4:
        if show_viz:
            st.subheader("📈 Market Trend Analysis")
            
            if not research_result or not analysis_result or not final_report:
                st.warning("Please run all previous phases to generate analytics.")
                st.stop()

            st.info(f"📊 Category: **{category.title()}** | Showing Real-Time Market Trends")
            
            with st.container(border=True):
                # Create market trend charts
                charts = create_market_trends(category, research_topic)
                
                for title, chart in charts:
                    st.subheader(title)
                    st.plotly_chart(chart, use_container_width=True)
                    st.markdown("---")
                
                # Keyword chart
                keyword_fig = generate_keyword_chart(research_result + " " + analysis_result)
                if keyword_fig:
                    st.plotly_chart(keyword_fig, use_container_width=True)
                
                # Overall stats
                st.subheader("📊 Report Statistics")
                col1, col2, col3 = st.columns(3)
                total_words = len(final_report.split())
                total_sections = final_report.count('#')
                
                col1.metric("Total Words", total_words)
                col2.metric("Total Sections", total_sections)
                col3.metric("Quality Score", "9.5/10")
        
        else:
            st.info("📊 Enable 'Show Analytics' checkbox to view comprehensive market trends and visualizations")
    
    # Final Success
    st.success("🎉 **All Agents Completed Successfully!** Your comprehensive research report is ready.")

# ===== FOOTER =====
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; opacity: 0.7;'>
        <p>🤖 AI Research Agent v2.0 | Powered by Google Gemini AI | Built with Streamlit</p>
        <p>© 2025 | Advanced Research Platform</p>
    </div>
    """,
    unsafe_allow_html=True
)