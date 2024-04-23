import Image from "next/image";

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-blue-500 to-indigo-600 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight sm:text-5xl md:text-6xl">
            Gutenberg Johanus: The AI Printing Press for Education
          </h1>
          <p className="mt-3 max-w-md mx-auto text-base text-gray-300 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
            Revolutionizing education through high-performance, scalable AI systems that deliver personalized learning experiences.
          </p>
        </div>

        <div className="mt-12 grid gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <Image
              src="/placeholder-image-1.jpg"
              alt="VectoDB Content Ingestion"
              width={500}
              height={300}
              priority
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900">VectoDB Content Ingestion</h3>
              <p className="mt-4 text-base text-gray-500">
                Our AI-powered system efficiently ingests content into VectoDB, enabling high-quality output and personalized learning experiences.
              </p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <Image
              src="/placeholder-image-2.jpg"
              alt="Personalized Educational Content"
              width={500}
              height={300}
              priority
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900">Personalized Educational Content</h3>
              <p className="mt-4 text-base text-gray-500">
                From writing coaches to math tutors, our AI generates tailored educational content to meet individual learning needs.
              </p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-lg overflow-hidden">
            <Image
              src="/placeholder-image-3.jpg"
              alt="AI-Powered Online School"
              width={500}
              height={300}
              priority
              className="w-full h-48 object-cover"
            />
            <div className="p-6">
              <h3 className="text-xl font-semibold text-gray-900">AI-Powered Online School</h3>
              <p className="mt-4 text-base text-gray-500">
                Our MVP is evolving into a comprehensive online school, leveraging AI to provide personalized learning experiences at scale.
              </p>
            </div>
          </div>
        </div>

        <div className="mt-16 text-center">
          <a
            href="/get-started"
            className="inline-block bg-white border border-transparent rounded-md py-3 px-8 font-medium text-blue-600 hover:bg-blue-50"
          >
            Get Started
          </a>
        </div>
      </div>
    </main>
  );
}