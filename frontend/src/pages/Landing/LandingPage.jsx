import Navbar from "../../components/layout/Navbar";
import hero from "../../assets/images/hero.svg";
import { motion } from "framer-motion";

function LandingPage() {
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

              <button className="bg-primary text-white px-8 py-4 rounded-full shadow-soft hover:scale-105 transition">

                Get Started

              </button>

              <button className="bg-white border border-primary text-primary px-8 py-4 rounded-full hover:bg-blue-50">

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
              alt="Hero"
              className="w-full"
            />

          </motion.div>

        </div>

      </section>

    </>
  );
}

export default LandingPage;