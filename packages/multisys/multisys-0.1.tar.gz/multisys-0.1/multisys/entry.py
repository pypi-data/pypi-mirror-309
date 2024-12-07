import argparse
from subprocess import Popen, PIPE, run

def build(path):
    if path == "":
        print('[WARN] No path provided. Using Local method.')
        print('Installing dependencies.. (build)')
        process = Popen(['pip', 'install','build'], stdout=PIPE, stderr=PIPE)
        print('Dependencies installed!')
        print('Building project..')
        process = Popen(['python', '-m', 'build'], stdout=PIPE, stderr=PIPE)
        print('Project has been built!')
        print('Finishing..')
        stdout, stderr = process.communicate()
    else:
        print('Path found! (Using Spec method)')
        print('Installing dependencies.. (build)')
        process = Popen(['pip', 'install','build'], stdout=PIPE, stderr=PIPE)
        print('Dependencies installed!')
        print('Building project..')
        process = Popen(['python', '-m', 'build'], stdout=PIPE, stderr=PIPE)
        print('Project has been built!')
        print('Finishing..')
        stdout, stderr = process.communicate()

def publish(dist):
    if dist == "" or dist == ".":
        print('[WARN] No dist provided. Using Local method.')
        print('Installing dependencies.. (twine)')
        proc = run(['pip', 'install', 'twine'])
        print('Dependencies installed!')
        print('Publishing project..')
        print('Finishing..')
        twine = run(['twine', 'upload', 'dist/*'])
    else:
        print('Dist was provided. Using Spec method')
        print('Installing dependencies.. (twine)')
        proc = run(['pip', 'install', 'twine'], stdout=PIPE, stderr=PIPE)
        print('Dependencies installed!')
        print('Publishing project..')
        print('Finishing..')
        twine = run(['twine', 'upload', dist], stdout=PIPE, stderr=PIPE)

def multisys_entry_point():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    parser_build = subparsers.add_parser('build', help='Builds your project')
    parser_build.add_argument('-p', '--path', help='The project path')
    
    parser_publish = subparsers.add_parser('publish', help='Publishes your project')
    parser_publish.add_argument('-d', '--dist', help='The location of the dist. (twine upload dist/*)')
    
    
    args = parser.parse_args()
    
    if args.command == 'build':
        build(args.path)
    elif args.command == 'publish':
        publish(args.dist)
    else:
        parser.print_help()
    