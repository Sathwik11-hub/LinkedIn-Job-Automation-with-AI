#!/usr/bin/env python3
"""
AutoAgentHire - Agent Runner Script
Run AI agents for job automation from command line.
"""
import asyncio
import argparse
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import after path setup
try:
    from backend.agents.orchestrator import AgentOrchestrator
    from backend.config import settings
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're in the project root and dependencies are installed")
    sys.exit(1)


async def run_job_search_workflow(args):
    """Run the job search workflow with given parameters."""
    print("🤖 Starting AutoAgentHire Job Search Workflow...")
    print(f"📝 Keywords: {args.keywords}")
    print(f"📍 Location: {args.location}")
    print(f"⭐ Experience: {args.experience}")
    print(f"💼 Job Type: {args.job_type}")
    print("-" * 50)
    
    try:
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        
        # Prepare search criteria
        search_criteria = {
            "keywords": args.keywords,
            "location": args.location,
            "experience_level": args.experience,
            "job_type": args.job_type,
            "max_results": args.max_results,
            "auto_apply": args.auto_apply
        }
        
        # Execute workflow
        print("🔍 Agent 1: Searching for jobs...")
        results = await orchestrator.execute_job_search_workflow(
            user_id=args.user_id,
            search_criteria=search_criteria
        )
        
        # Display results
        print(f"\n✅ Workflow Complete!")
        print(f"📊 Jobs Found: {results.get('jobs_found', 0)}")
        print(f"🎯 Applications Sent: {results.get('applications_sent', 0)}")
        print(f"⏱️  Execution Time: {results.get('execution_time', 'N/A')}")
        
        return results
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="AutoAgentHire - AI Job Automation Agent Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic job search
  python run_agents.py search --keywords "Python Developer" --location "San Francisco"
  
  # Advanced search with auto-apply
  python run_agents.py search --keywords "ML Engineer" --experience "Senior" --auto-apply
  
  # Remote jobs only
  python run_agents.py search --keywords "DevOps" --location "Remote" --job-type "Full-time"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Run job search workflow")
    search_parser.add_argument("--keywords", "-k", required=True, 
                              help="Job keywords (e.g., 'Python Developer')")
    search_parser.add_argument("--location", "-l", default="Remote",
                              help="Job location (default: Remote)")
    search_parser.add_argument("--experience", "-e", default="Mid Level",
                              choices=["Entry Level", "Mid Level", "Senior Level", "Lead/Principal"],
                              help="Experience level (default: Mid Level)")
    search_parser.add_argument("--job-type", "-t", default="Full-time",
                              choices=["Full-time", "Part-time", "Contract", "Internship"],
                              help="Job type (default: Full-time)")
    search_parser.add_argument("--max-results", "-m", type=int, default=50,
                              help="Maximum results to process (default: 50)")
    search_parser.add_argument("--user-id", "-u", default="cli_user",
                              help="User ID (default: cli_user)")
    search_parser.add_argument("--auto-apply", "-a", action="store_true",
                              help="Automatically apply to matching jobs")
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Check agent status")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == "search":
        # Run the async workflow
        results = asyncio.run(run_job_search_workflow(args))
        if results:
            print("\n🎉 Agent workflow completed successfully!")
        else:
            print("\n❌ Agent workflow failed!")
            sys.exit(1)
            
    elif args.command == "status":
        print("🤖 AutoAgentHire Agent Status:")
        print(f"📍 Project Root: {project_root}")
        print(f"⚙️  Environment: {settings.APP_ENV}")
        print(f"🔧 Debug Mode: {settings.DEBUG}")
        print("✅ All systems operational!")


if __name__ == "__main__":
    main()