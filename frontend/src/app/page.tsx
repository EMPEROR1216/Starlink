import PropertyInput from '@/components/PropertyInput';

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24 bg-gray-50">
      <div className="w-full max-w-5xl items-center justify-between font-mono text-sm">
        <p className="text-center w-full border-b border-gray-300 bg-gray-100 p-4">
          Starboard AI Agent Engineer Take-Home Challenge
        </p>
      </div>

      <div className="mt-16 flex flex-col items-center">
        <h1 className="text-3xl md:text-4xl font-bold text-center mb-2 text-gray-800">Industrial Property Analysis</h1>
        <p className="text-gray-600 mb-8">Enter a property address to find the best comparables.</p>
        
        {/* This is the component that was causing the error. 
            If the file exists in the right place, the error will go away. */}
        <PropertyInput />
      </div>
    </main>
  );
}