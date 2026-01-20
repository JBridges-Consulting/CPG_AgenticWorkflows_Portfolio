# Heritage Harvest | Field Intelligence & Revenue Recovery 🥔

An AI-powered category management engine designed to convert visual shelf audits into national revenue recovery strategies. This tool quantifies out-of-stock (OOS) leakage across a 1,200-store retail footprint using real-time computer vision and proprietary pricing data.

## 🛡️ Executive Revenue Recovery Blueprint
The core of this application is **Agent 3**, a Strategic Signal Monitor that identifies:
* **Competitive Gaps:** Pinpoints exactly where competitors are failing to maintain shelf stock.
* **Overskewed Analysis:** Analyzes shelf facings to identify slow-moving competitor SKUs that should be rationalized to make room for high-velocity Heritage Harvest products.
* **National Impact Math:** Automatically scales store-level voids to a 1,200-store chain-wide financial impact.

## 🚀 Key Features
* **Multi-Retailer Interface:** Dynamic environment selection for Retailer A, B, and C to provide bespoke reporting.
* **Computer Vision Integration:** Powered by GPT-4o for high-fidelity visual analysis of shelf conditions.
* **Financial Precision:** Integrates a local `pricing_master_UPSPW.csv` to ensure 100% accuracy in SKU pricing and velocity calculations.
* **Strategic Profit Recovery:** Generates an executive-ready summary focused on shelf optimization and immediate revenue capture.

## 🛠️ Setup & Installation
1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/JBridges-Consulting/Retail_Signal_Monitor.git](https://github.com/JBridges-Consulting/Retail_Signal_Monitor.git)
Configure Secrets: Add your OPENAI_API_KEY to the Streamlit Cloud Secrets dashboard or .streamlit/secrets.toml.Data Dependency: Ensure pricing_master_UPSPW.csv is present in the root directory for accurate revenue modeling.
📊 Commercial Impact LogicThe tool utilizes the following proprietary formula to quantify chain-wide opportunity:$$Total Weekly Chain Opportunity = \sum (List Price \times Weekly Velocity \times #of Stores)$$Developed for the Heritage Harvest National Account Team.

### **How to Update on GitHub:**
1. Go to your repository on GitHub.com.
2. Click on the **README.md** file.
3. Click the **pencil icon (edit)**.
4. Paste the code above and click **Commit changes**.
