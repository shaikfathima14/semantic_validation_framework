import Navbar from "../../components/layout/Navbar";
import hero from "../../assets/images/hero.svg";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";

function LandingPage() {
  const navigate = useNavigate();

  return (
    <>
      <Navbar />

      <section className="min-h-screen bg-background pt-28 px-8">

        <div className="max-w-7xl mx-auto grid lg:grid-cols-2 gap-12 items-center">

          {/* LEFT */}

          <motion.div
            initial={{ opacity: 0, x: -60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >

            <span className="inline-block bg-blue-100 text-primary px-4 py-2 rounded-full text-sm font-semibold">
              AI Powered E-Governance
            </span>

            <h1 className="text-6xl font-heading font-bold text-primary mt-6 leading-tight">
              Semantic Validation
            </h1>

            <h2 className="text-5xl font-heading text-gray-700">
              Framework
            </h2>

            <p className="mt-8 text-lg text-gray-600 leading-8">
              Enhance the reliability of citizen applications using
              Natural Language Processing and AI-powered semantic
              validation before government submission.
            </p>

            <div className="mt-8 space-y-3">

              <div>✔ Smart NLP Validation</div>

              <div>✔ Detect Missing Information</div>

              <div>✔ Improve Government Service Reliability</div>

            </div>

            <div className="mt-10 flex gap-5">

              {/* GET STARTED */}

              <button
                onClick={() => navigate("/dashboard")}
                className="bg-primary text-white px-8 py-4 rounded-full shadow-soft hover:scale-105 transition"
              >
                Get Started
              </button>

              {/* LEARN MORE */}

              <button
                onClick={() => {
                  document
                    .getElementById("about")
                    ?.scrollIntoView({ behavior: "smooth" });
                }}
                className="bg-white border border-primary text-primary px-8 py-4 rounded-full hover:bg-blue-50"
              >
                Learn More
              </button>

            </div>

          </motion.div>

          {/* RIGHT */}

          <motion.div
            initial={{ opacity: 0, x: 60 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
          >

            <img
              src={hero}
              alt="Semantic Validation"
              className="w-full"
            />

          </motion.div>

        </div>

        {/* ABOUT / LEARN MORE SECTION */}

        <section
          id="about"
          className="max-w-7xl mx-auto mt-24 pb-20"
        >

          <div className="bg-white rounded-3xl shadow-soft p-10">

            <h2 className="text-3xl font-bold text-primary mb-5">
              About SemanticAI
            </h2>

            <p className="text-gray-600 text-lg leading-8">
              SemanticAI is an AI-powered e-governance validation
              framework designed to analyze citizen documents before
              government submission.
            </p>

            <div className="grid md:grid-cols-3 gap-6 mt-8">

              <div className="bg-blue-50 rounded-2xl p-6">
                <h3 className="font-bold text-xl text-primary">
                  NLP Validation
                </h3>

                <p className="text-gray-600 mt-2">
                  Extracts and analyzes important information from
                  uploaded documents.
                </p>
              </div>

              <div className="bg-blue-50 rounded-2xl p-6">
                <h3 className="font-bold text-xl text-primary">
                  Error Detection
                </h3>

                <p className="text-gray-600 mt-2">
                  Detects missing, conflicting and inconsistent
                  information.
                </p>
              </div>

              <div className="bg-blue-50 rounded-2xl p-6">
                <h3 className="font-bold text-xl text-primary">
                  Smart Reports
                </h3>

                <p className="text-gray-600 mt-2">
                  Provides a clear validation score, errors and
                  warnings for the user.
                </p>
              </div>

            </div>

          </div>

        </section>

      </section>

    </>
  );
}

export default LandingPage;